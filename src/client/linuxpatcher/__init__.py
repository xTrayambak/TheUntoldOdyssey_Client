import subprocess
import distro

REDHAT_FAMILY = (
    "CentOS Linux", "Fedora Linux", "RHEL"
) # rpm

UBUNTU_FAMILY = (
    "Ubuntu", "Linux Mint", "Elementary OS", "Zorin OS"
) # apt

ARCH_FAMILY = (
    "Manjaro Linux", "Arch Linux", "BlackArch Linux", "Garuda Linux"
) # pacman

SUSE_FAMILY = (
    "OpenSUSE Linux"
) # zypper

def pacman_install(package: str):
    subprocess.call(
        ['pacman', '-S', package]
    )

def apt_install(package: str):
    subprocess.call(
        ['apt-get', 'install', package]
    )

def zypper_install(package: str):
    subprocess.call(
        ['zypper', 'install', package]
    )

def patch():
    distro_name = distro.name()
    if distro_name in REDHAT_FAMILY:
        pass
    elif distro_name in UBUNTU_FAMILY:
        apt_install("espeak")
        
    pass