import os

INSTALL_ESPEAK = "pacman -S espeak"
INSTALL_GLUT = "pacman -S freeglut"

def patch():
    os.system(INSTALL_ESPEAK)
    os.system(INSTALL_GLUT)