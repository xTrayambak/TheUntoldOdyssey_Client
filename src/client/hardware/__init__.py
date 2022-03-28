import sys
from src.log import *

class HardwareUtil:
    def __init__(self):
        self.gl_version = [0, 0, 0]
        self.gpu_vendor = "NOTDETECTED"
    
    def get(self):
        try:
            from pyglet.gl.gl_info import get_renderer, get_version, get_vendor
            gl_ver = []

            for idx, ver_no in enumerate(get_version().split(".")):
                if idx == 2:
                    break
                gl_ver.append(int(ver_no))

            self.gl_version = gl_ver
            self.gpu_vendor = get_vendor()
        except Exception as exc:
            log(exc)
            if sys.platform == 'linux':
                self.gl_version = [0, 0, 0]
                self.gpu_vendor = "LINUX-NOTDETECTED"