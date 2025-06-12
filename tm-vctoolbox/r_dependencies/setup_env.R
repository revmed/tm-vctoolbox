# --------------------------------------
# Project Environment Setup with `renv`
# --------------------------------------
# Run this script with `source("/path/to/setup_env.R")` in the R terminal only
# if initializing the environment for the first time.
# Once the setup script finishes executing, the `.Rprofile` should be created
# If you've already run this then you can just do `renv::restore()` in the R
# terminal if you already have the .lock file.

# ---- Special notes ----
# make sure your system already has the following:
# harbuzz fribidi freetype pkg-config libtiff libjpeg freetype
# If not, install them since some packages require native libraries to compile
# but they are not managed by R or `renv`
# -----------------------

# Install `renv` if it is not already installed
if (!requireNamespace("renv", quietly=TRUE)) {install.packages("renv")}

# Initialize `renv` in the current project directory
# This will create a local library and .Rprofile to isolate package dependencies
renv::init()

# These are the required packages for the renv-managed environment
required_packages = c(
  "this.path",
  "tidyverse",
  "RMariaDB",
  "config",
  "glue",
  "binom",
  "showtext",
  "ggrepel",
  "ggplot2",
  "ggsignif",
  "ggpubr",
  "ggsurvfit",
  "gtsummary",
  "rstatix",
  "argparse",
  "flextable",
  "kableExtra",
  "randomcoloR",
  "broom.helpers",
  "cardx",
  "openxlsx",
  "tibble",
  "tidyr",
  "purrr",
  "lubridate",
  "rlang",
  "yaml"
)

install.packages(required_packages, type="source")

biocpackages = c(
  "ComplexHeatmap"
)

if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install(biocpackages, force = TRUE)

# Snapshot the current pckage state into renv.lock
# Use the lock file to restore the exact package versions later
renv::snapshot()