# Do Frozen SMILES Embeddings Beat Fingerprints?

[![ChemRxiv](https://img.shields.io/badge/ChemRxiv-10.26434%2Fchemrxiv.15004188%2Fv1-blue)](https://doi.org/10.26434/chemrxiv.15004188/v1)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20142891.svg)](https://doi.org/10.5281/zenodo.20142891)

Public code and benchmark repository for:

**Do Frozen SMILES Foundation Embeddings Beat Fingerprints? A Split- and Low-Data Benchmark on ADMET and CNS Bioactivity Tasks**

This is a lightweight benchmark of cached frozen ChemBERTa and MoLFormer embeddings against Morgan fingerprints and RDKit descriptor baselines under random, scaffold, and low-data splits.

The ChemRxiv preprint is available at:

```text
https://doi.org/10.26434/chemrxiv.15004188/v1
```

The repository copy of the ChemRxiv PDF is available as [`paper.pdf`](paper.pdf). Reproducibility files remain organized under `scripts/`, `results/`, and `figures/`.

## Main Result

In the released benchmark, frozen-vs-classical comparisons are available for 43 dataset-regime rows across 8 curated binary tasks. The best Morgan/RDKit baseline wins 36/43 rows, while the best frozen embedding variant wins 7/43 rows. The clustered AUROC difference for frozen minus classical is -0.025 with a 95% CI of [-0.032, -0.018].

The message is narrow: frozen SMILES embeddings should be treated as candidate representations, not default replacements for strong fingerprint baselines.

## What Is Included

```text
paper.pdf               ChemRxiv preprint PDF
figures/                Main result figures for quick viewing
results/benchmark/      Summary tables and figures
scripts/                Benchmark and embedding scripts
data/README.md          Dataset placement notes
benchmark_config.yaml   Reproducible benchmark config
```

Raw datasets, LaTeX source drafts, `.env` files, API keys, model checkpoints, and large `.npy` embedding caches are intentionally not included.

## Repository And Archive

Preprint:

```text
https://doi.org/10.26434/chemrxiv.15004188/v1
```

Code and result artifacts:

```text
https://github.com/ItsTongKung/when-do-frozen-smiles-embeddings-beat-fingerprints
```

Frozen reproducibility artifact:

```text
https://doi.org/10.5281/zenodo.20142891
```

The GitHub repository is intended for code inspection and lightweight reruns. The ChemRxiv DOI should be used for citing the preprint, and the Zenodo DOI should be used for citing the versioned reproducibility artifact.

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

## Citation

Use `CITATION.cff` or cite the ChemRxiv preprint:

```text
Sriwicha, P. Do Frozen SMILES Foundation Embeddings Beat Fingerprints?
A Split- and Low-Data Benchmark on ADMET and CNS Bioactivity Tasks.
ChemRxiv, 2026. https://doi.org/10.26434/chemrxiv.15004188/v1
```

For the reproducibility artifact, cite Zenodo DOI `10.5281/zenodo.20142891`.

## License

Repository code is released under the MIT license. The ChemRxiv preprint is posted under CC-BY-NC 4.0, as indicated on the ChemRxiv record.
