import sys
from src.log import *

class HardwareUtil:
    def __init__(self):
        self.gl_version = [0, 0, 0]
        self.gpu_vendor = "NOTDETECTED"
    
    def get(self):
        try:
            from pyglet.gl.gl_info import get_renderer, get_version, get_vendor
            raw_gl_ver_dt = get_version().split(".")
            gl_ver = [
                int(raw_gl_ver_dt[0]), int(raw_gl_ver_dt[1].split(" ")[0]) # what the hell?
            ]

            self.gl_version = gl_ver
            self.gpu_vendor = get_vendor()
            self.gl_version_string_detailed = get_version()
        except Exception as exc:
            warn(exc, "Worker/HardwareDetector")
            if sys.platform == 'linux':
                self.gl_version = [0, 0]
                self.gpu_vendor = "LINUX-NOTDETECTED"