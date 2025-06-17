"""
Script to compare DataFrame outputs from R and Python
"""

# %%
from pathlib import Path

import pandas as pd

from tm_vctoolbox.utils_rpy2 import RScriptRunner, compare_r_py_dataframes

# %%
#  Set filepaths
path_to_renv = Path.home() / "Developer/repos"
path_to_repo = Path.home() / "Developer/repos"
path_to_script = path_to_repo / "tm-graph2/lib/master/query_edc_master.R"

# %%
# Instantiate the RScriptRunner with the path to the renv and the script
runner = RScriptRunner(path_to_renv, path_to_script)

# %%
# Call the R function to pull EDC master data
df_rpy2 = runner.call(
    "pull_edc_master",
    compound_study="6236-001",
    edc_table="edc_overview",
)
print(f"Shape of df_rpy2: {df_rpy2.shape}")

# %%
#  read in the CSV output from R
df_r = pd.read_csv(
    path_to_repo / "tm-vctoolbox/tm_vctoolbox/rpy2_scratchpad/edc_overview_test.csv"
)
print(f"Shape of df_r: {df_r.shape}")

# %%
# Sort both DataFrames by columns to ensure they are comparable
col_order = df_rpy2.columns.tolist()
df_rpy2_sorted = df_rpy2.reset_index(drop=True)
df_r_sorted = df_r.loc[:, col_order].reset_index(drop=True)

# df_r_sorted = fix_r_dataframe_types(df_r_sorted)  # Clean R-specific issues
# df_rpy2_sorted, df_r_sorted = normalize_dtypes(df_rpy2_sorted, df_r_sorted)
# df_rpy2_sorted, df_r_sorted = align_numeric_dtypes(df_rpy2_sorted, df_r_sorted)


are_equal = df_rpy2_sorted.equals(df_r_sorted)
print("DataFrames are equal (sorted):", are_equal)

# %%
# Compare the sorted DataFrames
diff_sorted = df_rpy2_sorted.compare(df_r_sorted)
print("Differences after resetting index:")
print(diff_sorted)


# %%
results = compare_r_py_dataframes(df_rpy2_sorted, df_r_sorted)

if results["shape_mismatch"]:
    print("Shape mismatch detected.")

if results["columns_mismatch"]:
    print("Column names differ.")

if results["index_mismatch"]:
    print("Indexes differ.")

if results["numeric_diffs"]:
    print("Numeric differences found:")
    for col, diffs in results["numeric_diffs"].items():
        print(f"\nColumn: {col}")
        print(diffs)

if results["non_numeric_diffs"]:
    print("Non-numeric differences found:")
    for col, diffs in results["non_numeric_diffs"].items():
        print(f"\nColumn: {col}")
        print(diffs)

if (
    not results["shape_mismatch"]
    and not results["columns_mismatch"]
    and not results["index_mismatch"]
    and not results["numeric_diffs"]
    and not results["non_numeric_diffs"]
):
    print("DataFrames are equivalent (within tolerance).")


# %%
print(df_rpy2.loc[:, "Cohort"].iloc[450])
print(df_r.loc[:, "Cohort"].iloc[450])

# %%
