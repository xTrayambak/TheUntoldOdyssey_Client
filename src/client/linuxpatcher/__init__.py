"""
Buggy as hell Linux patcher. May fix it once I have an actual team of programmers.
"""

import distro
import elevate
import os
import subprocess
from pymsgbox import alert, confirm

from src.client.io import IOFile
from src.log import log, warn

current_uid_before_escalate = os.getuid()
current_wdir_before_escalate = os.getcwd()

def elevate_privileges(b: bool = True):
    """
    Escalate privileges of the TUO process to execute the package managers.

    TODO: Find any bugs to make sure no RCEs are possible.
    """
    # elevate
    if b:
        warn("Elevating privileges of TUO process!", "Worker/PrivilegeEscalator")
        elevate.elevate(False)
        # so, it seems it sets our current working directory to /root/ automatically after escalation...
        os.chdir(current_wdir_before_escalate)
        print(f"SET DIRECTORY TO '{current_wdir_before_escalate}' AGAIN!")

    # unelevate
    else:
        warn("De-escalating privileges of TUO process.", "Worker/PrivilegeEscalator")
        subprocess.call(
            [
                'su', '-', ' $(id', '-un', f'{current_uid_before_escalate})'
            ]
        )

    return os.getuid() == 0

def pacman_install(package: str):
    subprocess.call(
        ['sudo', 'pacman', '-S', package]
    )

def yay_install(package: str):
    # AUR moment.
    subprocess.call(
        ['yay', '-S', package]
    )

def apt_install(package: str):
    subprocess.call(
        ['sudo', 'apt-get', 'install', package]
    )

def zypper_install(package: str):
    subprocess.call(
        ['sudo', 'zypper', 'ins', package]
    )

def patch():
    # check if it's already patched.
    f_confirm_lnx_patch = IOFile.new('assets/LINUX_PATCHED', 'r')
    if f_confirm_lnx_patch.readline(0) == '1':
       f_confirm_lnx_patch.close()
       return

    # consent is a good thing. (please do not take out of context)
    do_patch = confirm("It looks like you're using Linux, TUO needs to install some libraries to work properly, if you do not agree, then TUO may crash or some features may get auto-disabled by the game which affect QOL or accessibility. Syntax has a very privacy focused ideology and cares about if you consent to this. The TUO process will gain root privileges and install the libraries needed from your package manager.", "TUO Linux Patcher - Consent to elevate privileges.", ("Elevate and Install (recommended)", "Do not install anything. (not recommended)"))
    if do_patch != 'Elevate and Install (recommended)':
        warn("The user has told us explicitly not to install libraries needed.", "Worker/LinuxPatcher")
        return

    result = elevate_privileges()

    if not result:
        warn("Failed to elevate privileges to ROOT, aborting patching process.", "Worker/LinuxPatcher")
        return
    elif result:
        log("Elevated TUO process successfully!", "Worker/LinuxPatcher")

    distro_name = distro.like()

    if distro_name == 'arch':
        pacman_install('python-espeak')
    elif distro_name == 'debian':
        apt_install('espeak')

    f_confirm_lnx_patch.change_mode('w')
    f_confirm_lnx_patch.write('1')
