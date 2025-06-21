"""
This module contains functions for cleaning and standardizing data
"""

# %%
import numpy as np
import pandas as pd


# %%
def correct_time_points(
    df,
    patient_id_col="Patient_ID",
    visit_name_col="Visit_name",
    treatment_cat_col="Treatment_Category",
):
    """
    Assign treatment categories ("Pre", "On", "End") to patient visits in a dataframe.

    For each patient group (grouped by `patient_id_col`), the function:
    - Converts "NA" strings in the treatment category column to pd.NA.
    - Checks if categories "Pre", "On", or "End" are already assigned anywhere in the patient group.
    - For each row with missing category (NaN), assigns category based on the visit name only if
      that category is not already assigned anywhere in the group:
        - Visits "C1D1" or "SCREENING" get category "Pre" if no "Pre" assigned yet.
        - Visits "C2D1" or "C3D1" get category "On" if no "On" assigned yet.
        - Visit "EOT" gets category "End" if no "End" assigned yet.
    - Keeps existing categories unchanged.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing patient visit data.
    patient_id_col : str, default "Patient_ID"
        Name of the column identifying patients.
    visit_name_col : str, default "Visit_name"
        Name of the column containing visit names.
    treatment_cat_col : str, default "Treatment_Category"
        Name of the column to assign/update treatment categories.

    Returns:
    --------
    pandas.DataFrame
        A copy of the input dataframe with updated treatment categories.
    """
    df = df.copy()

    def assign_group(group):
        # Convert "NA" string to pd.NA in treatment category column
        group[treatment_cat_col] = group[treatment_cat_col].replace("NA", pd.NA)

        # Check if categories already assigned anywhere in the group
        has_pre = group[treatment_cat_col].eq("Pre").any()
        has_on = group[treatment_cat_col].eq("On").any()
        has_end = group[treatment_cat_col].eq("End").any()

        def assign_row(row):
            vn = row[visit_name_col]
            tc = row[treatment_cat_col]

            if pd.isna(tc):
                if vn in ["C1D1", "SCREENING"] and not has_pre:
                    return "Pre"
                elif vn in ["C2D1", "C3D1"] and not has_on:
                    return "On"
                elif vn == "EOT" and not has_end:
                    return "End"
                else:
                    return pd.NA
            else:
                return tc

        group[treatment_cat_col] = group.apply(assign_row, axis=1)
        return group

    return df.groupby(patient_id_col, group_keys=False).apply(assign_group)


# %%
def set_plot_indication(df, indication_map, col_name="Indication", default="OTHER"):
    """
    Adds a new column 'Plot_Indication' to the DataFrame using a mapping dictionary.

    For each row, the value in the specified column (default: 'Indication') is mapped to a new value
    using the provided indication_map. If the value is not found in the mapping, the default value is used.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame with an indication column (default: 'Indication').
    indication_map : dict
        Dictionary mapping indication values to desired plot indication values.
    col_name : str, optional
        Name of the column to map from (default is 'Indication').
    default : str, optional
        Default value for Plot_Indication if the indication is not in the mapping (default is "OTHER").

    Returns
    -------
    pandas.DataFrame
        DataFrame with an added 'Plot_Indication' column reflecting the mapped values.

    Example Usage
    -------------
    indication_map = {
        "LUNG": "NSCLC",
        "COLORECTAL": "CRC",
        "PANCREATIC": "PDAC",
        # Add more mappings as needed
    }

    annotation_df = set_plot_indication(annotation_df, indication_map)
    """
    df = df.copy()
    df["Plot_Indication"] = df[col_name].map(indication_map).fillna(default)
    return df


# %%
