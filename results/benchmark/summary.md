# Local-v3 benchmark summary

Completed fits: 2580
Datasets: 8
Models: chemberta_lr, chemberta_rf, chemberta_xgb, molformer_lr, molformer_rf, molformer_xgb, morgan_lr, morgan_rf, morgan_xgb, rdkit_lr, rdkit_rf, rdkit_xgb

## Overall AUROC by split and family

| split       | model_family   |   auroc |
|:------------|:---------------|--------:|
| lowdata_100 | classical      |   0.746 |
| lowdata_100 | foundation     |   0.721 |
| lowdata_250 | classical      |   0.781 |
| lowdata_250 | foundation     |   0.752 |
| lowdata_50  | classical      |   0.719 |
| lowdata_50  | foundation     |   0.702 |
| lowdata_500 | classical      |   0.771 |
| lowdata_500 | foundation     |   0.732 |
| random      | classical      |   0.829 |
| random      | foundation     |   0.798 |
| scaffold    | classical      |   0.774 |
| scaffold    | foundation     |   0.754 |

## Best model per dataset/split

| dataset                                               | split       | best_model    | family     |   auroc |
|:------------------------------------------------------|:------------|:--------------|:-----------|--------:|
| B3DB_Classification                                   | lowdata_100 | rdkit_rf      | classical  |   0.811 |
| BBB_Martins                                           | lowdata_100 | rdkit_rf      | classical  |   0.856 |
| Bioavailability_Ma                                    | lowdata_100 | chemberta_xgb | foundation |   0.650 |
| ChEMBL_CNS_CHEMBL217_D2_dopamine_receptor             | lowdata_100 | morgan_rf     | classical  |   0.748 |
| ChEMBL_CNS_CHEMBL228_Sodiumdependent_serotonin_transp | lowdata_100 | morgan_rf     | classical  |   0.861 |
| ChEMBL_CNS_CHEMBL233_Mutype_opioid_receptor           | lowdata_100 | morgan_rf     | classical  |   0.879 |
| HIA_Hou                                               | lowdata_100 | rdkit_lr      | classical  |   0.877 |
| PAMPA_NCATS                                           | lowdata_100 | rdkit_xgb     | classical  |   0.652 |
| B3DB_Classification                                   | lowdata_250 | rdkit_rf      | classical  |   0.837 |
| BBB_Martins                                           | lowdata_250 | morgan_rf     | classical  |   0.860 |
| Bioavailability_Ma                                    | lowdata_250 | chemberta_xgb | foundation |   0.684 |
| ChEMBL_CNS_CHEMBL217_D2_dopamine_receptor             | lowdata_250 | morgan_rf     | classical  |   0.839 |
| ChEMBL_CNS_CHEMBL233_Mutype_opioid_receptor           | lowdata_250 | morgan_xgb    | classical  |   0.909 |
| HIA_Hou                                               | lowdata_250 | chemberta_lr  | foundation |   0.904 |
| PAMPA_NCATS                                           | lowdata_250 | rdkit_rf      | classical  |   0.694 |
| B3DB_Classification                                   | lowdata_50  | rdkit_rf      | classical  |   0.791 |
| BBB_Martins                                           | lowdata_50  | rdkit_rf      | classical  |   0.812 |
| Bioavailability_Ma                                    | lowdata_50  | rdkit_rf      | classical  |   0.632 |
| ChEMBL_CNS_CHEMBL217_D2_dopamine_receptor             | lowdata_50  | morgan_rf     | classical  |   0.741 |
| ChEMBL_CNS_CHEMBL228_Sodiumdependent_serotonin_transp | lowdata_50  | morgan_rf     | classical  |   0.831 |
| ChEMBL_CNS_CHEMBL233_Mutype_opioid_receptor           | lowdata_50  | morgan_xgb    | classical  |   0.848 |
| HIA_Hou                                               | lowdata_50  | rdkit_rf      | classical  |   0.842 |
| PAMPA_NCATS                                           | lowdata_50  | rdkit_rf      | classical  |   0.644 |
| B3DB_Classification                                   | lowdata_500 | morgan_rf     | classical  |   0.871 |
| BBB_Martins                                           | lowdata_500 | morgan_rf     | classical  |   0.900 |
| Bioavailability_Ma                                    | lowdata_500 | morgan_lr     | classical  |   0.717 |
| PAMPA_NCATS                                           | lowdata_500 | rdkit_rf      | classical  |   0.728 |
| B3DB_Classification                                   | random      | morgan_rf     | classical  |   0.942 |
| BBB_Martins                                           | random      | morgan_rf     | classical  |   0.923 |
| Bioavailability_Ma                                    | random      | morgan_rf     | classical  |   0.734 |
| ChEMBL_CNS_CHEMBL217_D2_dopamine_receptor             | random      | morgan_rf     | classical  |   0.847 |
| ChEMBL_CNS_CHEMBL228_Sodiumdependent_serotonin_transp | random      | morgan_lr     | classical  |   0.907 |
| ChEMBL_CNS_CHEMBL233_Mutype_opioid_receptor           | random      | morgan_xgb    | classical  |   0.916 |
| HIA_Hou                                               | random      | chemberta_xgb | foundation |   0.942 |
| PAMPA_NCATS                                           | random      | rdkit_rf      | classical  |   0.756 |
| B3DB_Classification                                   | scaffold    | morgan_rf     | classical  |   0.892 |
| BBB_Martins                                           | scaffold    | morgan_rf     | classical  |   0.900 |
| Bioavailability_Ma                                    | scaffold    | rdkit_rf      | classical  |   0.715 |
| ChEMBL_CNS_CHEMBL217_D2_dopamine_receptor             | scaffold    | chemberta_rf  | foundation |   0.725 |
| ChEMBL_CNS_CHEMBL228_Sodiumdependent_serotonin_transp | scaffold    | morgan_rf     | classical  |   0.852 |
| ChEMBL_CNS_CHEMBL233_Mutype_opioid_receptor           | scaffold    | morgan_rf     | classical  |   0.897 |
| HIA_Hou                                               | scaffold    | chemberta_lr  | foundation |   0.933 |
| PAMPA_NCATS                                           | scaffold    | chemberta_xgb | foundation |   0.728 |
