# Do Frozen SMILES Embeddings Beat Fingerprints?

Public code and benchmark repository for:

**Do Frozen SMILES Foundation Embeddings Beat Fingerprints? A Split- and Low-Data Benchmark on ADMET and CNS Bioactivity Tasks**

This is a lightweight benchmark of cached frozen ChemBERTa and MoLFormer embeddings against Morgan fingerprints and RDKit descriptor baselines under random, scaffold, and low-data splits.

## Main Result

In the released benchmark, frozen-vs-classical comparisons are available for 43 dataset-regime rows across 8 curated binary tasks. The best Morgan/RDKit baseline wins 36/43 rows, while the best frozen embedding variant wins 7/43 rows. The clustered AUROC difference for frozen minus classical is -0.025 with a 95% CI of [-0.032, -0.018].

The message is narrow: frozen SMILES embeddings should be treated as candidate representations, not default replacements for strong fingerprint baselines.

## What Is Included

```text
figures/                Main result figures for quick viewing
results/benchmark/      Summary tables and figures
scripts/                Benchmark and embedding scripts
data/README.md          Dataset placement notes
benchmark_config.yaml   Reproducible benchmark config
```

Raw datasets, paper drafts, `.env` files, API keys, model checkpoints, and large `.npy` embedding caches are intentionally not included.

## Reproduce

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts\prepare_embeddings.py
python scripts\summarize_embeddings.py
python scripts\run_benchmark.py --config benchmark_config.yaml
```

The source tables must first be placed in `data/`; see `data/README.md`.

## Suggested GitHub Settings

Repository name:

```text
when-do-frozen-smiles-embeddings-beat-fingerprints
```

Description:

```text
Split- and low-data benchmark of frozen ChemBERTa/MoLFormer embeddings against Morgan/RDKit baselines for ADMET and CNS bioactivity tasks.
```

Topics:

```text
cheminformatics, molecular-property-prediction, admet, chemberta, molformer, rdkit, xgboost, machine-learning
```

Recommended first tag:

```text
v0.1.0
```

## Citation

Use `CITATION.cff`. After the GitHub URL and arXiv ID are available, update the citation metadata and README.
