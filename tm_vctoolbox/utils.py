"""
File containing some general purpose code for manipulating data
"""

# %%
import inspect
import os


# %%
def get_func_dir(func):
    """
    Return the directory path of the source file where the given function is defined.

    Parameters:
        func (function): The function object to inspect.

    Returns:
        str: Absolute directory path of the file containing the function definition.
    """
    # Get the source file where the function is defined
    filename = inspect.getfile(func)
    # Return the directory of that file
    return os.path.dirname(os.path.abspath(filename))


# %%
def get_current_dir():
    """
    Return the directory path of the source file where the caller function is defined.

    Inspects the call stack to find the immediate caller's source file.

    Returns:
        str: Absolute directory path of the file containing the caller function.
    """
    # Get the current frame
    current_frame = inspect.currentframe()
    # The caller frame is one level up
    caller_frame = current_frame.f_back

    # Get the filename where the caller function is defined
    filename = inspect.getfile(caller_frame)

    # Get the directory of that filename
    return os.path.dirname(os.path.abspath(filename))
