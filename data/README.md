# Data

Raw datasets are not included in this GitHub-ready folder.

Expected files:

```text
bbb_martins.tab
b3db_classification.tab
hia_hou.tab
bioavailability_ma.tab
pampa_ncats.tab
chembl_cns_targets.csv
```

Generated embedding arrays are also ignored by git. Regenerate them with:

```powershell
python scripts\prepare_embeddings.py
```
