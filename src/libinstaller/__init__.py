from src.log import log

from os import system
from pkg_resources import get_distribution, DistributionNotFound

LIBRARIES = open("assets/requirements", "r").readlines()

def exists(package: str):
    try:
        dist = get_distribution(package)
        return True
    except DistributionNotFound:
        return False

def install(_lib: str):
    ### This function was optimized in 0.0.5, it now checks if the package exists instead of mindlessly trying to install it, which makes bootup faster. ###
    if exists(_lib): return
    lib = str(_lib).split("\n")[0]
    log("Installing '{}', querying PyPi through os.system()".format(lib), "Worker/LibraryHandler")
    result = system("python -m pip install {}".format(lib))
    log("Got result code [{}] after requesting to install library.".format(result), "Worker/LibraryHandler")

def installAllLibraries():
    log("Attempting to install all libraries from PyPi.", "Worker/LibraryHandler")
    for _lib in LIBRARIES:
        install(_lib)