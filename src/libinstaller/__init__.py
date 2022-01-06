from subprocess import check_call as call
from sys import executable
from pkg_resources import get_distribution, DistributionNotFound

def log(msg):
    print(f"Pre-Client Initialization >> {msg}")

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
        if exists(lib): return
        log("Installing library [{}]; querying PyPi.")
        
        call(
            [executable, "-m", "pip", "install", lib]
        )