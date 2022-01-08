from subprocess import check_call as call
from sys import executable
from pkg_resources import get_distribution, DistributionNotFound

from src.log import warn, log

def exists(package: str):
    try:
        dist = get_distribution(package)
        return True
    except DistributionNotFound:
        return False

def installAllLibraries():
    libs = open("assets/requirements").readlines()

    for lib in libs:
        lib = lib.split("\n")[0]
        if not exists(lib):
            warn(f"Library '{lib}' is not installed for the virtual environment.")
            log(f"Installing library [{lib}]; querying PyPi.")
        
            call(
                [executable, "-m", "pip", "install", lib]
            )