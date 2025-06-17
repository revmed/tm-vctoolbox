library(tidyverse)
library(dplyr)
library(this.path)
library(fs)

# Load the utility functions. Using this since I am in the different directory
lib_path <- normalizePath(file.path("tm-graph2/lib"))

query_edc_master <- rlang::env()
source(this.proj(lib_path, "master/query_edc_master.R"), local = query_edc_master)

utility_libs <- rlang::env()
source(this.proj(lib_path, "utility_libs.R"), local = utility_libs)


# Get dataframe from EDC master
df <- query_edc_master$pull_edc_master("6236-001")

# Construct output filepath
output_filepath <- path_home() / "Developer/repos/tm-vctoolbox/tm_vctoolbox/rpy2_scratchpad" / "edc_overview_test.csv"

# Make sure directory exists
dir.create(dirname(output_filepath), recursive = TRUE, showWarnings = FALSE)

# Assume df is your data frame
df[] <- lapply(df, function(x) if (is.factor(x)) as.character(x) else x)
write.csv(df, file = output_filepath, row.names = FALSE, na = "", fileEncoding = "UTF-8")


# Message to confirm save
cat("Saved CSV to:", output_filepath, "\n")
