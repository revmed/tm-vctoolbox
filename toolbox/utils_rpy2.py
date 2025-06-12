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

        from rpy2 import robjects
        from rpy2.robjects import pandas2ri, conversion
        from rpy2.robjects.conversion import get_conversion

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
