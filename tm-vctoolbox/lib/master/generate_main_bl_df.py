"""
This file is dependent on the R functions written in `tm-graph2`
You should have the repo cloned somewhere and use those filepaths.
This one focuses on the `generate_main_bl_df.R`
"""
# %%
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
pandas2ri.activate()
from rpy2.robjects.packages import importr
from utils_rpy2 import activate_renv

# %%
runner = RScriptRunner(Path("/path/to/script.R"))
df = runner.call("generate_master_main_bl_df", "6236-001")

# %%
