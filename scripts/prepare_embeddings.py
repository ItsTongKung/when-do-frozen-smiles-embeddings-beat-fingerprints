"""Generate frozen ChemBERTa and MoLFormer embedding caches.

This script reads public molecular-property tables from ``data/`` and writes
mean-pooled frozen encoder embeddings next to those tables. The cached arrays
are intentionally ignored by git because they are derived, machine-generated
artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import types
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from transformers import AutoModel, AutoTokenizer


MODEL_CONFIGS = {
    "chemberta": {
        "model_id": "seyonec/ChemBERTa-zinc-base-v1",
        "filename_suffix": "seyonec_ChemBERTa_zinc_base_v1_meanpool_v3",
        "trust_remote_code": False,
        "max_length": 256,
        "batch_size": 128,
    },
    "molformer": {
        "model_id": "ibm-research/MoLFormer-XL-both-10pct",
        "filename_suffix": "ibm_research_MoLFormer_XL_both_10pct_meanpool_v3",
        "trust_remote_code": True,
        "max_length": 202,
        "batch_size": 64,
    },
}


SOURCE_BUNDLES = {
    "BBB_Martins": ("bbb_martins.tab", "\t", "Drug"),
    "B3DB_Classification": ("b3db_classification.tab", "\t", "Drug"),
    "HIA_Hou": ("hia_hou.tab", "\t", "Drug"),
    "Bioavailability_Ma": ("bioavailability_ma.tab", "\t", "Drug"),
    "PAMPA_NCATS": ("pampa_ncats.tab", "\t", "Drug"),
    "ChEMBL_CNS_targets": ("chembl_cns_targets.csv", ",", "canonical_smiles"),
}


def patch_molformer_transformers5() -> None:
    """Compatibility patch for the MoLFormer remote code under transformers 5."""
    onnx_mod = types.ModuleType("transformers.onnx")

    class OnnxConfig:  # pragma: no cover - only used by remote config import
        pass

    onnx_mod.OnnxConfig = OnnxConfig
    sys.modules.setdefault("transformers.onnx", onnx_mod)

    import transformers.pytorch_utils as pytorch_utils

    if not hasattr(pytorch_utils, "find_pruneable_heads_and_indices"):

        def find_pruneable_heads_and_indices(heads, n_heads, head_size, already_pruned_heads):
            mask = torch.ones(n_heads, head_size)
            heads = set(heads) - already_pruned_heads
            for head in heads:
                head = head - sum(1 if h < head else 0 for h in already_pruned_heads)
                mask[head] = 0
            mask = mask.view(-1).contiguous().eq(1)
            index = torch.arange(len(mask))[mask].long()
            return heads, index

        pytorch_utils.find_pruneable_heads_and_indices = find_pruneable_heads_and_indices


def read_smiles(data_root: Path, bundle: str) -> list[str]:
    filename, sep, smiles_col = SOURCE_BUNDLES[bundle]
    df = pd.read_csv(data_root / filename, sep=sep)
    smiles = df[smiles_col].fillna("").astype(str).tolist()
    return smiles


def set_molformer_deterministic(model) -> None:
    model.get_head_mask = lambda head_mask, num_hidden_layers: [None] * num_hidden_layers
    if hasattr(model, "config"):
        model.config.deterministic_eval = True
    for module in model.modules():
        if hasattr(module, "deterministic"):
            module.deterministic = True


def mean_pool(last_hidden: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    mask = attention_mask.unsqueeze(-1).to(last_hidden.dtype)
    return (last_hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)


def embed_smiles(
    smiles: list[str],
    model_key: str,
    device: torch.device,
) -> tuple[np.ndarray, dict]:
    cfg = MODEL_CONFIGS[model_key]
    if model_key == "molformer":
        patch_molformer_transformers5()
        torch.manual_seed(0)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(0)
    tokenizer = AutoTokenizer.from_pretrained(
        cfg["model_id"],
        trust_remote_code=bool(cfg["trust_remote_code"]),
    )
    model = AutoModel.from_pretrained(
        cfg["model_id"],
        trust_remote_code=bool(cfg["trust_remote_code"]),
    )
    if model_key == "molformer":
        set_molformer_deterministic(model)
    model.to(device)
    model.eval()

    rows: list[np.ndarray] = []
    t0 = time.perf_counter()
    with torch.no_grad():
        for start in range(0, len(smiles), int(cfg["batch_size"])):
            batch = smiles[start : start + int(cfg["batch_size"])]
            enc = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=int(cfg["max_length"]),
                return_tensors="pt",
            )
            enc = {k: v.to(device) for k, v in enc.items()}
            out = model(**enc)
            last_hidden = out.last_hidden_state if hasattr(out, "last_hidden_state") else out[0]
            pooled = mean_pool(last_hidden, enc["attention_mask"]).detach().cpu().numpy().astype(np.float32)
            rows.append(pooled)
    elapsed = time.perf_counter() - t0
    arr = np.vstack(rows)
    metadata = {
        "model": cfg["model_id"],
        "dim": int(arr.shape[1]),
        "n": int(arr.shape[0]),
        "pooling": "attention-mask mean pooling over last hidden state",
        "max_length": int(cfg["max_length"]),
        "batch_size": int(cfg["batch_size"]),
        "device": str(device),
        "torch_dtype": "float32",
        "transformers_trust_remote_code": bool(cfg["trust_remote_code"]),
        "molformer_seed": 0 if model_key == "molformer" else None,
        "molformer_deterministic_eval": True if model_key == "molformer" else None,
        "elapsed_s": float(elapsed),
    }
    return arr, metadata


def write_bundle(data_root: Path, bundle: str, model_key: str, force: bool, device: torch.device) -> None:
    cfg = MODEL_CONFIGS[model_key]
    out = data_root / f"{bundle}_{cfg['filename_suffix']}_embeddings.npy"
    meta = data_root / f"{bundle}_{cfg['filename_suffix']}_embeddings.metadata.json"
    if out.exists() and meta.exists() and not force:
        print(f"[skip] {out.name}")
        return
    smiles = read_smiles(data_root, bundle)
    print(f"[embed] {bundle} {model_key} n={len(smiles)}")
    arr, metadata = embed_smiles(smiles, model_key, device)
    metadata.update({"bundle": bundle, "source_rows": len(smiles)})
    np.save(out, arr)
    meta.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"[wrote] {out} shape={arr.shape}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--models", nargs="+", choices=sorted(MODEL_CONFIGS), default=sorted(MODEL_CONFIGS))
    parser.add_argument("--bundles", nargs="+", choices=sorted(SOURCE_BUNDLES), default=sorted(SOURCE_BUNDLES))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    device = torch.device(args.device)
    for model_key in args.models:
        for bundle in args.bundles:
            write_bundle(args.data_root, bundle, model_key, args.force, device)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
