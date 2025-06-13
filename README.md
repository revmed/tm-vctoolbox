# tm-vctoolbox

General purpose Python toolbox for translational medicine and data science workflows, with utilities for integrating R code and data analysis pipelines.

---
# Project Structure

```
tm-vctoolbox/
├── main.py
├── pyproject.toml
├── tm_vctoolbox/
│   ├── __init__.py
│   ├── plots.py
│   ├── utils.py
│   ├── utils_rpy2.py
│   ├── test_r_functions.py
│   ├── test_r_functions.R
│   ├── lib/
│   │   └── master/
│   │       └── generate_main_bl_df.py
│   └── r_dependencies/
│       ├── setup_env.R
│       └── README.md
├── tests/
│   └── ... (test files)
└── README.md
```

## Contents

- **main.py**: Entry point for the package (prints a hello message).
- **tm_vctoolbox/**: Main package directory.
  - **plots.py**: Plotting utilities (details not shown here).
  - **utils.py**: General Python utility functions.
  - **utils_rpy2.py**: Utilities for calling R functions from Python using `rpy2`, including:
    - `activate_renv`: Activates an R `renv` environment from Python.
    - `RScriptRunner`: Class for sourcing R scripts and calling R functions.
    - `r_namedlist_to_dict`: Converts R named lists to Python dictionaries.
  - **test_r_functions.py**: Example/test code for calling R functions from Python, including:
    - Loading and activating an R `renv` environment.
    - Calling R functions that return scalars or data frames.
    - Converting between pandas DataFrames and R data.frames.
  - **test_r_functions.R**: Example R script with functions to be called from Python.
  - **lib/master/generate_main_bl_df.py**: Example of using `RScriptRunner` to call an R function from the `tm-graph2` repo.
  - **r_dependencies/**: R environment setup scripts and documentation.
    - **setup_env.R**: Script to initialize an R `renv` environment and install required R packages.
    - **README.md**: Instructions for setting up the R environment.


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

- R >= 4.4.1
- [`renv`](https://rstudio.github.io/renv/) for R package management
- [See `r_dependencies/setup_env.R`](tm_vctoolbox/r_dependencies/setup_env.R) for the full list of required R packages (e.g., `tidyverse`, `argparse`, `ComplexHeatmap`, `reticulate`, etc.)

#### R Environment Setup

1. Install system libraries (macOS: run `install_r_dev_deps_homebrew.sh` if present).
2. Initialize the R environment:
   ```r
   source("/path/to/tm_vctoolbox/r_dependencies/setup_env.R")
   ```
   This will create a local renv environment and install all required R packages.
3. To restore on a new machine:
   ```r
   renv::restore()
   ```

See `r_dependencies/README.md` for more details.

---

## How to Use

### Calling R Functions from Python

1. Make sure your R environment is set up and renv is initialized.
2. Use the utilities in `utils_rpy2.py` to activate the R environment and call R functions.

**Example:**

```python
from pathlib import Path
from tm_vctoolbox.utils_rpy2 import RScriptRunner, r_namedlist_to_dict

# Set paths
path_to_renv = Path.home() / "Developer/repos"
path_to_script = path_to_renv / "tm-graph2/lib/master/generate_main_bl_df.R"

# Initialize runner and call R function
runner = RScriptRunner(path_to_renv, path_to_script)
result = runner.call("generate_master_main_bl_df", "6236-001", assay="all")
result_dict = r_namedlist_to_dict(result)
print(result_dict["df"])
```

See `test_r_functions.py` for more usage examples, including conversion between pandas and R data frames.

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

