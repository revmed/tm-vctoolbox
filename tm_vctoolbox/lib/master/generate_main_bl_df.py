"""
This file is dependent on the R functions written in `tm-graph2`
You should have the repo cloned somewhere and use those filepaths.
This one focuses on the `generate_main_bl_df.R`
"""

# %%
from pathlib import Path
from tm_vctoolbox.utils_rpy2 import RScriptRunner, r_namedlist_to_dict


# %%
# Activate renv where the `renv` is located
path_to_renv = Path.home() / "Developer/repos"
path_to_repo = Path.home() / "Developer/repos"
path_to_script = path_to_repo / "tm-graph2/lib/master/generate_main_bl_df.R"

# # %%
# call_r_script_function(
#     path_to_renv, path_to_script, "generate_master_main_bl_df", "6236-001"
# )

# %%
# put full filepath to where `generate_main_bl_df.R`
runner = RScriptRunner(path_to_renv, path_to_script)
df_list = runner.call("generate_master_main_bl_df", "6236-001", assay="all")
res_dict = r_namedlist_to_dict(df_list)
print(res_dict.keys())
res_dict["df"]
len(res_dict["patient_ids"]["# patients in EDC"])

# %%
# TODO: convert this to a function
