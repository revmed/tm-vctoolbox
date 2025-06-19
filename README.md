# tm-vctoolbox

General purpose Python toolbox for translational medicine and data science workflows, with utilities for integrating R code and data analysis pipelines.

This repo uses [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management and [rpy2](https://rpy2.readthedocs.io/en/latest/) for R integration.

If you git clone this repo, you can run `make install` to set up the Python environment and install all dependencies. The package will install in editable mode, so you can modify the code and see changes immediately.

To create a virtual environment, run:
```sh
uv venv
```

To activate the virtual environment, run:
```sh
source .venv/bin/activate
```

To add as a python kernel for Jupyter notebooks/IPython, run:
```sh
uv run --python3 -- -m ipykernel install --user --name tm-vctoolbox --display-name "tm-vctoolbox"
```

---

# Project Structure

```
tm-vctoolbox/
├── main.py
├── pyproject.toml
├── tm_vctoolbox/
│   ├── __init__.py
│   ├── plotting/
│   │   ├── plots.py
│   │   └── rvmd_style.py
│   ├── utils.py
│   ├── utils_rpy2.py
│   ├── rpy2_scratchpad/
│   │   ├── test_r_functions.py
│   │   ├── test_r_functions.R
│   │   ├── compare_r_py_df_outputs.py
│   │   └── generate_edc_csv.R
│   └── r_dependencies/
│       ├── setup_env.R
│       ├── install_r_dev_deps_homebrew.sh
│       ├── .Rversion
│       └── README.md
├── uv.lock
├── .python-version
├── Makefile
├── .gitignore
└── README.md
```

## Contents

- **main.py**: Entry point for the package (prints a hello message).
- **tm_vctoolbox/**: Main package directory.
  - **plotting/**: Plotting utilities and RVMD style definitions.
    - `plots.py`: Example code for generating tables and exporting to PowerPoint/PDF.
    - `rvmd_style.py`: Custom fonts, color palettes, and matplotlib themes for RVMD.
  - **utils.py**: General Python utility functions.
  - **utils_rpy2.py**: Utilities for calling R functions from Python using `rpy2`, including:
    - `activate_renv`: Activates an R `renv` environment from Python.
    - `RScriptRunner`: Class for sourcing R scripts and calling R functions.
    - `r_namedlist_to_dict`: Converts R named lists to Python dictionaries.
    - DataFrame post-processing and comparison utilities.
  - **rpy2_scratchpad/**: Example/test code for R/Python interoperability.
    - `test_r_functions.py`/`.R`: Example R script and Python code for calling R functions and converting DataFrames.
    - `compare_r_py_df_outputs.py`: Compare DataFrame outputs from R and Python.
    - `generate_edc_csv.R`: Example R script for generating CSVs for comparison.
    - `example_rscript_runner.py`: Example of using `RScriptRunner` to call an R function from the `tm-graph2` repo.
  - **r_dependencies/**: R environment setup scripts and documentation.
    - `setup_env.R`: Script to initialize an R `renv` environment and install required R packages.
    - `install_r_dev_deps_homebrew.sh`: Installs system libraries for R packages (macOS/Homebrew).
    - `.Rversion`: R version pinning.
    - `README.md`: Instructions for setting up the R environment.

---

## Dependencies

### Python

- Python >= 3.11
- [See `pyproject.toml`](pyproject.toml) for full list, including:
  - `rpy2` (for R integration)
  - `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotnine`, `scikit-learn`, `scipy`, `statannotations`, `umap`, `pycomplexheatmap`
  - Development: `pytest`, `ruff`, `isort`, `black`

Install all dependencies (main + dev) with:
```sh
make install-all
```
or just main dependencies:
```sh
make install
```

### R

- R >= 4.4.1 (see [`.Rversion`](tm_vctoolbox/r_dependencies/.Rversion))
- [`renv`](https://rstudio.github.io/renv/) for R package management
- [See `r_dependencies/setup_env.R`](tm_vctoolbox/r_dependencies/setup_env.R) for the full list of required R packages (e.g., `tidyverse`, `argparse`, `ComplexHeatmap`, `reticulate`, etc.)

#### R Environment Setup

1. **Install system libraries** (macOS: run `install_r_dev_deps_homebrew.sh` if present):
    ```sh
    chmod +x tm_vctoolbox/r_dependencies/install_r_dev_deps_homebrew.sh
    ./tm_vctoolbox/r_dependencies/install_r_dev_deps_homebrew.sh
    ```
2. **Initialize the R environment**:
    Open the integrated R terminal in VSCode and run:
    ```r
    source("/path/to/tm_vctoolbox/r_dependencies/setup_env.R")
    ```
    This will create a local renv environment and install all required R packages.
3. **To restore on a new machine**:
    ```r
    renv::restore()
    ```
4. **Snapshot changes** (if you add new packages):
    ```r
    install.packages("new_package")
    renv::snapshot()
    ```

See [`r_dependencies/README.md`](tm_vctoolbox/r_dependencies/README.md) for more details and troubleshooting.

---

## How to Use

### Calling R Functions from Python

1. Make sure your R environment is set up and renv is initialized.
2. Use the utilities in [`utils_rpy2.py`](tm_vctoolbox/utils_rpy2.py) to activate the R environment and call R functions.

**Example:**

```python
from pathlib import Path
from tm_vctoolbox.utils_rpy2 import RScriptRunner

# Set paths
path_to_renv = Path.home() / "Developer/repos"
path_to_script = path_to_renv / "tm-graph2/lib/master/generate_main_bl_df.R"

# Initialize runner and call R function
runner = RScriptRunner(path_to_renv, path_to_script)
res = runner.call("generate_master_main_bl_df", "6236-001", assay="all")
print(res["df"])
```

See [`rpy2_scratchpad/test_r_functions.py`](tm_vctoolbox/rpy2_scratchpad/test_r_functions.py) for more usage examples, including conversion between pandas and R data frames.

---

## Development

- Format code: `make format`
- Lint code: `make lint`
- Run tests: `pytest`

---

## Notes

- You must have R installed and accessible in your environment.
- The package is designed to work with R projects managed by renv.
- For R/Python interoperability, the [reticulate](https://rstudio.github.io/reticulate/) package is also recommended on the R side.
- See [`tm_vctoolbox/r_dependencies/README.md`](tm_vctoolbox/r_dependencies/README.md) for VSCode R extension and configuration tips.
- Always restart your R session after installing system libraries.
- Run `renv::status()` anytime to check if your environment is consistent.
- Use `renv::diagnostics()` if something breaks (this checks your setup).
- In your `.RProfile`, you may want to add:
    ```r
    # Activate renv
    source("/path/to/renv/activate.R")

    # Activate Python virtual environment via reticulate
    library(reticulate)
    use_virtualenv("/path/to/tm-vctoolbox/.venv", required = TRUE)
    ```
- In your `~/.zshrc`, you may want to add:
    ```
    export PATH="/path/to/tm-vctoolbox/.venv/bin:$PATH"
    ```

