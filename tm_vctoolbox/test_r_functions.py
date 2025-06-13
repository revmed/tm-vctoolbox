# %%
#  --------------------------------------------------------------------
#  This chunk here shows how to load the `renv` if that is being used
#  --------------------------------------------------------------------
from pathlib import Path
from rpy2 import robjects
from tm_vctoolbox.utils_rpy2 import activate_renv

# Activate renv environment by sourcing the activate function
activate_renv(Path.home() / "Developer/repos")

# Now load your R script and call functions e.g. below
# robjects.r.source("test_r_functions.R")
# data_proc_fn = robjects.r["my_data_processing_function"]

# Continue with your pandas -> R conversion and function call...

# %%
#  ---------------------------------------------------------------
#  Use this chunk here to load simple functions that are not dfs
#  ---------------------------------------------------------------
from pathlib import Path
from rpy2 import robjects
from tm_vctoolbox.utils_rpy2 import activate_renv

# Activate renv environment by sourcing the activate function
activate_renv(Path.home() / "Developer/repos")

# Load the R script containing your custom function
robjects.r.source("test_r_functions.R")

# Get your custom R function as a Python object
addition_fn = robjects.r["my_addition_function"]

# Call the R function with Python arguments
result = addition_fn(5, 3)

# Print the result (which will be an R object, possibly needing conversion)
print(result)

# If needed, convert the R result to a Python object
# (e.g., to a float if the result is a single numeric value)
python_result = float(result[0])
print(python_result)


# %%
#  -----------------------------------------------------------
#  Use this chunk here to load functions that return dfs/dts
#  -----------------------------------------------------------
from pathlib import Path
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2 import robjects
import pandas as pd
from tm_vctoolbox.utils_rpy2 import activate_renv

# Activate renv environment by sourcing the activate function
activate_renv(Path.home() / "Developer/repos")

# Load R script
robjects.r.source("test_r_functions.R")
data_proc_fn = robjects.r["my_data_processing_function"]

# Create a pandas DataFrame
df = pd.DataFrame({"numbers": [5, 3]})

# Convert pandas -> R
with localconverter(robjects.default_converter + pandas2ri.converter):
    r_df = robjects.conversion.py2rpy(df)

# Call the R function
r_result = data_proc_fn(r_df)

# Convert R -> pandas
with localconverter(robjects.default_converter + pandas2ri.converter):
    result_df = robjects.conversion.rpy2py(r_result)

print(result_df)

# %%
