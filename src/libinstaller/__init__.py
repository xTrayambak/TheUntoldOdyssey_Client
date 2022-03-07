from subprocess import check_call as call
from sys import executable
from pkg_resources import get_distribution, DistributionNotFound

from src.log import warn, log

def exists(package: str):
    """
    Check if a package exists in our current virtual runtime environment/Python interpreter instance.
    """
    try:
        get_distribution(package)
        return True
    except DistributionNotFound:
        return False

def installAllLibraries():
    """
    Check if all the libraries required for the game to run are installed or not, if not, then install them
    by querying PyPi through `py -m pip install <package>`
    """
    libs = open("assets/requirements").readlines()

    for lib in libs:
        lib = lib.split("\n")[0]
        log(f"Checking if library '{lib}' is installed or not.", "Worker/Requirements")
        if not exists(lib):
            warn(f"Library '{lib}' is not installed for the virtual environment.")
            log(f"Installing library [{lib}]; querying PyPi.")
        
            call(
                [executable, "-m", "pip", "install", lib]
            )