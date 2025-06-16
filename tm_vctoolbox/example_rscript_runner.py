"""
This file demonstrates how to use the `RScriptRunner` class to run R scripts.

Successful code execution is dependent on the R functions written in `tm-graph2`

You should have the repo cloned somewhere and use those filepaths.
"""

# %%
from pathlib import Path

from tm_vctoolbox.utils_rpy2 import RScriptRunner, r_namedlist_to_dict

# %%
# Activate renv where the `renv` is located
path_to_renv = Path.home() / "Developer/repos"
path_to_repo = Path.home() / "Developer/repos"

# %%
# below is an example of how to run the `generate_main_bl_df.R` script using the RScriptRunner
path_to_script = path_to_repo / "tm-graph2/lib/master/generate_main_bl_df.R"

# put full filepath to where `generate_main_bl_df.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df_list = runner.call("generate_master_main_bl_df", "6236-001", assay="all")
res_dict = r_namedlist_to_dict(df_list)
print(res_dict.keys())
res_dict["df"]
len(res_dict["patient_ids"]["# patients in EDC"])

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
print(res_dict["MR_data"])

# %%
