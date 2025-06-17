"""
This file demonstrates how to use the `RScriptRunner` class to run R scripts.

Successful code execution is dependent on the R functions written in `tm-graph2`

You should have the repo cloned somewhere and use those filepaths.
"""

# %%
from pathlib import Path

import pandas as pd

from tm_vctoolbox.utils_rpy2 import RScriptRunner, r_namedlist_to_dict

# %%
# Activate renv where the `renv` is located
path_to_renv = Path.home() / "Developer/repos"
# set path_to_renv = None if renv is not used
path_to_repo = Path.home() / "Developer/repos"
# %%
# below is an example of how to run the `generate_main_bl_df.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/generate_main_bl_df.R"

# put full filepath to where `generate_main_bl_df.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df_list = runner.call("generate_master_main_bl_df", "6236-001", assay="all")
res_dict = r_namedlist_to_dict(df_list)
print(list(res_dict.keys()))
df = res_dict["df"]
print(df.head())

#  this would bring back what the values in count table map to
count_table_map = dict()
for k, v in res_dict["patient_ids"].items():
    count_table_map[k] = len(v)

print(
    pd.DataFrame.from_dict(
        count_table_map, orient="index", columns=["count"]
    ).sort_values("count", ascending=False)
)

# %%
# below is an example of how to run the `generate_main_eot_df.R` script using the RScriptRunner
# TODO: this script is not working as expected, need to fix it somewhere?
# RuntimeError: Error calling R function 'generate_master_main_eot_df': Error in list(EOT_Failure = qc1, Non_Acquired_Variants = qc2, Non_EOT_Patients = qc3,  : argument 4 is empty
path_to_script = path_to_repo / "tm-graph2/lib/master/generate_main_eot_df.R"

# put full filepath to where `generate_main_eot_df.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df_list = runner.call(
    "generate_master_main_eot_df", "6236-001", edc_table="edc_overview"
)
res_dict = r_namedlist_to_dict(df_list)
print(res_dict.keys())

# %%
# below is an example of how to run the `generate_main_mr_df.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/generate_main_mr_df.R"

# put full filepath to where `generate_main_mr_df.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df_list = runner.call("generate_master_main_mr_df", "6236-001", enrollment_filter="yes")
res_dict = r_namedlist_to_dict(df_list)
print(res_dict.keys())

# this table has the main df of info
df = res_dict["MR_data"]
print(df.head())

# %%
# This script only works since I dropped the `**- comments` columns from the table on the R side
# Below is an example of how to run the `query_edc_master.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/query_edc_master.R"

# put full filepath to where `query_edc_master.R`
runner = RScriptRunner(path_to_renv, path_to_script)

# # check rlang::env()
# utility_libs_path = (
#     Path.home() / "Developer/repos/tm-graph2/lib/utility_libs.R"
# ).as_posix()
# robjects.r("utility_libs <- rlang::env()")
# robjects.r(f'source("{utility_libs_path}", local = utility_libs)')

# utility_libs = robjects.r["utility_libs"]

# get_config_file = utility_libs.find("get_config_file")
# config_path = get_config_file()[0]
# print("Config path:", config_path)


df = runner.call(
    "pull_edc_master",
    compound_study="6236-001",
    edc_table="edc_overview",
)
print(df.head())

# %%
# Below is an example of how to run the `query_guardant_master.R` script using the RScriptRunner
# This script only works since I dropped the `**- comments` columns from the table on the R side
path_to_script = path_to_repo / "tm-graph2/lib/master/query_guardant_master.R"

# put full filepath to where `query_guardant_master.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df = runner.call("pull_guardant_query_master", "6236-001", edc_table="edc_overview")
print(df.head())


# %%
# Below is an example of how to run the `query_ras_mutation_master.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/query_ras_mutation_master.R"

# put full filepath to where `query_ras_mutation_master.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df = runner.call("pull_ras_mutation_master_query", "6236-001", edc_table="edc_overview")
print(df.head())

# %%
# Below is an example of how to run the `query_scan_master.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/query_scan_master.R"

# put full filepath to where `query_scan_master.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df = runner.call("pull_scan", "6236-001")
print(df.head())

# %%
# This script only works since I dropped the `**- comments` columns from the table on the R side
# Below is an example of how to run the `query_screening_master.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/query_screening_master.R"

# put full filepath to where `query_screening_master.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df = runner.call("pull_screening_query_master", "6236-001", edc_table="edc_overview")
print(df.head())

# %%
# This script only works since I dropped the `**- comments` columns from the table on the R side
# Below is an example of how to run the `query_biodesix_master.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/query_biodesix_master.R"

# put full filepath to where `query_biodesix_master.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df = runner.call("pull_biodesix_data", "6236-001")
print(df.head())

# %%
