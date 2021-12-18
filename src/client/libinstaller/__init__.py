from src.client.log import log

from os import system

LIBRARIES = open("assets/requirements", "r").readlines()

def install(_lib: str):
    lib = str(_lib).split("\n")[0]
    log("Installing '{}', querying PyPi through os.system()".format(lib), "Worker/LibraryHandler")
    result = system("python -m pip install {}".format(lib))
    log("Got result code [{}] after requesting to install library.".format(result), "Worker/LibraryHandler")

def installAllLibraries():
    log("Attempting to install all libraries from PyPi.", "Worker/LibraryHandler")
    for _lib in LIBRARIES:
        install(_lib)