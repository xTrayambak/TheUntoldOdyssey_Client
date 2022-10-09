#!/usr/bin/env python

from src.client.ui.image import Image

class ImageLoader:
    def __init__(self, tuo):
        self.tuo = tuo

    def compat_conv_pos(self, pos):
        final = [0, 0, 0]
        if pos[0] == None:
            # LUA handler
            final[0] = pos[1]
            final[1] = pos[2]
            final[2] = pos[3]
        else:
            final = pos

        return final

    def load_image(self, path: str, pos: tuple = (0, 0, 0), scale: float | int = None):
        img = Image(path, pos, None, scale)

        return img
