from subprocess import check_call as call
from sys import executable, platform
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
    libs = open("requirements.txt").readlines()

    for lib in libs:
        if lib.startswith('#'): continue
        
        # Your CPU fans will make demonic screeching noises whilst running this segment of code. I am to blame, but you will never catch me alive!!!!!!!
        if lib.startswith('!!windows!!') and platform not in ('win32', 'win64'): continue
        if lib.startswith('!!mac!!') and platform != 'darwin': continue
        if lib.startswith('!!linux!!') and platform != 'linux': continue

        lib = lib.replace('!!windows!!', '', 1)
        lib = lib.replace('!!mac!!', '', 1)
        lib = lib.replace('!!linux!!', '', 1)

        lib = lib.split("\n")[0]
        log(f"Checking if library '{lib}' is installed or not.", "Worker/Requirements")
        if not exists(lib):
            warn(f"Library '{lib}' is not installed for the virtual environment.", "Worker/LibInstaller")
            log(f"Installing library [{lib}]; querying PyPi.", "Worker/LibInstaller")
        
            try:
                call(
                    [executable, "-m", "pip", "install", lib]
                )
            except Exception as exc:
                warn(f"An error occured whilst trying to install a library: [{exc}]", "Worker/LibInstaller")
