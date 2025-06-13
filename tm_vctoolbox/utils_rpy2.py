"""
Wrapper for calling R functions from Python using rpy2.

----------
** R must be installed and accessible in your environment **
Ensure compatibility with your R project's renv setup.
----------
"""

# %%
# Import libraries
import os
from pathlib import Path

from rpy2 import robjects
from rpy2.rlike.container import NamedList
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.vectors import (
    BoolVector,
    FloatVector,
    IntVector,
    ListVector,
    StrVector,
)


# %%
def activate_renv(path_to_renv: Path):
    """
    Activates the renv environment using renv::load() to ensure the correct project is loaded.
    This avoids sourcing activate.R directly and avoids accidentally initializing a new environment.
    """
    renv_project_dir = path_to_renv.resolve()
    renv_activate = renv_project_dir / "renv" / "activate.R"
    renv_lock = renv_project_dir / "renv.lock"

    if not renv_activate.exists() or not renv_lock.exists():
        raise FileNotFoundError(
            f"[Error] renv environment not found or incomplete at: {renv_project_dir}"
        )

    # Optional: set R_ENVIRON_USER if .Renviron exists
    renviron_file = renv_project_dir / ".Renviron"
    if renviron_file.is_file():
        os.environ["R_ENVIRON_USER"] = str(renviron_file)
        print("[Info] R_ENVIRON_USER set to:", renviron_file)

    # Load the renv environment using renv::load(path)
    try:
        robjects.r(f'renv::load("{renv_project_dir.as_posix()}")')
        print(f"[Info] renv environment loaded for project: {renv_project_dir}")
    except Exception as e:
        raise RuntimeError(f"[Error] Failed to load renv environment: {e}")

    print(".libPaths()")
    print(robjects.r(".libPaths()"))


# %%
class RScriptRunner:
    """
    A utility class to load and execute R functions from a specified R script using rpy2.
    """

    def __init__(self, path_to_renv: Path, script_path: Path):
        if not script_path.exists():
            raise FileNotFoundError(f"R script not found: {script_path}")

        self.path_to_renv = path_to_renv.resolve()
        self.script_path = script_path.resolve()
        self.script_dir = self.script_path.parent

        self._load_script()

    def _load_script(self):
        """
        Set the R working directory and source the R script.
        """
        activate_renv(self.path_to_renv)

        robjects.r(f'setwd("{self.script_dir.as_posix()}")')
        robjects.r(f'source("{self.script_path.as_posix()}")')
        print(f"[Info] R script sourced: {self.script_path.name}")

    def call(self, function_name: str, *args, **kwargs):
        """
        Call a function defined in the sourced R script and convert the result to Python.
        """
        try:
            r_func = robjects.globalenv[function_name]

            with localconverter(robjects.default_converter + pandas2ri.converter):
                r_args = [robjects.conversion.py2rpy(arg) for arg in args]
                r_kwargs = {k: robjects.conversion.py2rpy(v) for k, v in kwargs.items()}
                result = r_func(*r_args, **r_kwargs)
                return robjects.conversion.rpy2py(result)

        except KeyError:
            raise ValueError(f"Function '{function_name}' not found in the R script.")
        except Exception as e:
            raise RuntimeError(f"Error calling R function '{function_name}': {e}")


# %%
def r_namedlist_to_dict(namedlist):
    """
    Recursively convert an R NamedList or ListVector to a Python dictionary,
    unwrap R vectors (StrVector, IntVector, etc.) into Python lists,
    and convert data.frames to pandas DataFrames.
    """
    # If it is a named list or list vector, convert recursively to dict
    if isinstance(namedlist, (NamedList, ListVector)):
        result = {}
        for key, value in zip(namedlist.names(), namedlist):
            result[key] = r_namedlist_to_dict(value)
        return result

    # If it's an atomic vector (str, int, float, bool), convert to Python list
    if isinstance(namedlist, (StrVector, IntVector, FloatVector, BoolVector)):
        return list(namedlist)

    # For data frames and other R objects, use pandas2ri conversion if possible
    with localconverter(robjects.default_converter + pandas2ri.converter):
        try:
            py_obj = robjects.conversion.rpy2py(namedlist)
            return py_obj
        except Exception:
            # fallback to returning as-is if conversion fails
            return namedlist
