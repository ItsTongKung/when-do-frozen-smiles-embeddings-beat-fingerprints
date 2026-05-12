"""Summarize frozen embedding cache metadata.

The benchmark intentionally reports downstream classifier runtime separately
from embedding generation. This helper turns the generated embedding metadata
and tokenizer truncation diagnostics into a compact CSV table used by the
paper writer.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from prepare_embeddings import MODEL_CONFIGS, SOURCE_BUNDLES, patch_molformer_transformers5, read_smiles


DISPLAY_ENCODER = {
    "chemberta": "ChemBERTa",
    "molformer": "MoLFormer",
}


def metadata_path(data_root: Path, bundle: str, model_key: str) -> Path:
    suffix = MODEL_CONFIGS[model_key]["filename_suffix"]
    return data_root / f"{bundle}_{suffix}_embeddings.metadata.json"


def embedding_path(data_root: Path, bundle: str, model_key: str) -> Path:
    suffix = MODEL_CONFIGS[model_key]["filename_suffix"]
    return data_root / f"{bundle}_{suffix}_embeddings.npy"


def truncation_stats(smiles: list[str], model_key: str) -> dict[str, float | int]:
    cfg = MODEL_CONFIGS[model_key]
    if model_key == "molformer":
        patch_molformer_transformers5()
    tokenizer = AutoTokenizer.from_pretrained(
        cfg["model_id"],
        trust_remote_code=bool(cfg["trust_remote_code"]),
    )
    lengths = [
        len(tokenizer(str(smi), add_special_tokens=True, truncation=False)["input_ids"])
        for smi in smiles
    ]
    max_length = int(cfg["max_length"])
    truncated = [length > max_length for length in lengths]
    return {
        "max_tokenized_length": int(max(lengths) if lengths else 0),
        "mean_tokenized_length": float(sum(lengths) / len(lengths)) if lengths else 0.0,
        "truncated_count": int(sum(truncated)),
        "truncation_rate": float(sum(truncated) / len(lengths)) if lengths else 0.0,
    }


def summarize(data_root: Path) -> pd.DataFrame:
    rows: list[dict] = []
    truncation_cache: dict[tuple[str, str], dict[str, float | int]] = {}
    for bundle in SOURCE_BUNDLES:
        smiles = read_smiles(data_root, bundle)
        for model_key, cfg in MODEL_CONFIGS.items():
            meta_file = metadata_path(data_root, bundle, model_key)
            embed_file = embedding_path(data_root, bundle, model_key)
            if not meta_file.exists() or not embed_file.exists():
                continue
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            stats_key = (bundle, model_key)
            if stats_key not in truncation_cache:
                truncation_cache[stats_key] = truncation_stats(smiles, model_key)
            trunc = truncation_cache[stats_key]
            elapsed_s = float(meta.get("elapsed_s", 0.0))
            n = int(meta.get("n", len(smiles)))
            rows.append(
                {
                    "bundle": bundle,
                    "encoder": DISPLAY_ENCODER[model_key],
                    "checkpoint": str(cfg["model_id"]),
                    "n_molecules": n,
                    "elapsed_s": elapsed_s,
                    "molecules_per_s": float(n / elapsed_s) if elapsed_s > 0 else float("nan"),
                    "device": str(meta.get("device", "")),
                    "max_length": int(meta.get("max_length", cfg["max_length"])),
                    "max_tokenized_length": trunc["max_tokenized_length"],
                    "mean_tokenized_length": trunc["mean_tokenized_length"],
                    "truncated_count": trunc["truncated_count"],
                    "truncation_rate": trunc["truncation_rate"],
                    "embedding_disk_mb": float(embed_file.stat().st_size / (1024 * 1024)),
                }
            )
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/benchmark/tables/embedding_generation_summary.csv"),
    )
    args = parser.parse_args()
    df = summarize(args.data_root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
