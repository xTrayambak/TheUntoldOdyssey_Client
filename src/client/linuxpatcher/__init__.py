import os

INSTALL_ESPEAK = "pacman -Sy espeak"
INSTALL_GLUT = "pacman -Sy freeglut"

def patch():
    os.system(INSTALL_ESPEAK)
    os.system(INSTALL_GLUT)