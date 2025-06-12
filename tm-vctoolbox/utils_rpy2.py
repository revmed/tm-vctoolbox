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
import sys
import shutil
from pathlib import Path

from rpy2 import robjects
from rpy2.robjects import pandas2ri, conversion
from rpy2.robjects.conversion import get_conversion, localcoverter

# %%
def activate_renv(project_path: Path):
    """
    Activate renv environment for the given R project path.
    Project path refers to the path in which the `renv` is located.
    """
    renv_activate = project_path / "renv" / "activate.R"
    renviron_file = project_path / ".Renviron"

    if not renv_activate.is_file():
        print(f"[Warning] renv activation script not found at: {renv_activate}")
    else:
        os.environ["R_PROFILE_USER"] = str(renv_activate)
        print("[Info] renv activation script set.")

    if renviron_file.is_file():
        os.environ["R_ENVIRON_USER"] = str(renviron_file)
        print("[Info] .Renviron file set.")


class RFunctionCaller:
    def __init__(self, project_path: Path = None, auto_convert: bool = True):
        if shutil.which("R") is None:
            print("[Error] R is not installed or not found in system PATH.")
            sys.exit(1)

        if project_path:
            activate_renv(project_path)

        self.robjects = robjects
        self.pandas2ri = pandas2ri
        self.conversion = conversion
        self.get_conversion = get_conversion

        self.converter = get_conversion()
        if auto_convert:
            self.converter = self.converter + pandas2ri.converter

        self.auto_convert = auto_convert

    def call(self, func_name, *args, convert=None, **kwargs):
        """
        Call an R function by name with the given arguments.

        Args:
            func_name (str): Name of the R function to call.
            *args: Positional arguments.
            convert (bool or None): Override auto_convert for this call.
            **kwargs: Named arguments.

        Returns:
            Converted result if enabled, else raw R object.
        """
        try:
            r_func = self.robjects.r[func_name]
            use_convert = self.auto_convert if convert is None else convert

            with self.conversion.localconverter(
                self.converter if use_convert else self.get_conversion()
            ):
                r_args = [self._to_r(arg) for arg in args]
                r_kwargs = {k: self._to_r(v) for k, v in kwargs.items()}
                result = r_func(*r_args, **r_kwargs)
                return self.conversion.rpy2py(result) if use_convert else result

        except Exception as e:
            print(f"[RFunctionCaller] Error calling '{func_name}': {e}")
            return None

    def _to_r(self, obj):
        """Convert Python object to R, unless it's already an R object."""
        if isinstance(obj, self.robjects.RObject):
            return obj
        return self.conversion.py2rpy(obj)


# %%
class RScriptRunner:
    """
    A utility class to load and execute R functions from a specified R script using rpy2.

    This class handles:
    - Sourcing an R script.
    - Setting the R working directory.
    - Calling R functions with arguments.
    - Converting R return values to Python objects (e.g., pandas DataFrames).

    Example usage:
        runner = RScriptRunner(Path("path/to/script.R"))
        res = runner.call("my_r_function", arg1, arg2)
    """

    def __init__(self, script_path: Path):
        """
        Initialize the RScriptRunner with the path to an R script.

        Parameters:
            script_path (Path): Full path to the R script to be sourced.

        Raises:
            FileNotFoundError: If the script file does not exist.
        """
        if not script_path.exists():
            raise FileNotFoundError(f"R script not found: {script_path}")
        self.script_path = script_path
        self.script_dir = script_path.parent
        self._load_script()

    def _load_script(self):
        """
        Internal method to set the R working directory and source the R script.
        """
        robjects.r['setd')
        robjects.r(f'source("{self.script_path}")')

    def call(self, function_name: str, *args):
        """
        Call a function defined in the sourced R script and convert the result to Python.

        Parameters:
            function_name (str): Name of the R function to call.
            *args: Arguments to pass to the R function.

        Returns:
            Python object: The result of the R function converted to a Python object.

        Raises:
            ValueError: If the function is not found in the R global environment.
            RuntimeError: If the function call fails.
        """
        try:
            r_func = robjects.globalenv[function_name]
            r_res = r_func(*args)
            with localconverter(robjects.default_converter + pandas2ri.converter):
                return robjects.conversion.rpy2py(r_res)
        except KeyError:
            raise ValueError(f"Function '{function_name}' not found in the R script.")
        except Exception as e:
            raise RuntimeError(f"Error calling R function '{function_name}': {e}")
