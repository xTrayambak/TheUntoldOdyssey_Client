#!/usr/bin/env python3
"""
Library for loading in shaders, automatically loads in any folder inside /assets/shaders and searches for vert.glsl and frag.glsl and loads 'em in.

Do not read, 5 years of my life have been cut off because of this atrocity.
"""

import os
from panda3d.core import Shader

from src.client.loader import getAsset
from src.log import log, warn

SHADER_DIRECTORY = getAsset("shader_directory", "path")

VERT_NAME = "vert.glsl"
FRAG_NAME = "frag.glsl"

def loadAllShaders():
    shaders = []
    shader_dirs = os.scandir(SHADER_DIRECTORY)
    for obj in shader_dirs:
        """idx = shader_dirs.index(_dir)
        if idx == len(shader_dirs): break
        ## hacky way to load in the shaders, since os.walk is a dumpster fire of a function. :-)
        _origin = _dir[0]
        dir = _dir[1]
        print(type(dir))
        dir = dir[0]
        _vert, _frag = _origin + dir + "/" + VERT_NAME, dir +"/"+ FRAG_NAME
        ## i have no idea what cells in my brain sparked up to create this abomination of a solution
        ## rewrite later, please!!! i beg you!!
        # - trayambak"""
        # ok, time to fix this. takes forever to load shaders, probs the main boot-up bottleneck.
        
        if obj.is_file(): break

        dir = obj.name
        path = SHADER_DIRECTORY + dir
        _vert = path + "/" +VERT_NAME
        _frag = path + "/" +FRAG_NAME

        log(f"Loading shader <{dir}>", "Worker/ShaderLoader")
        _shdr = Shader.load(
            Shader.SL_GLSL,
            vertex = _vert,
            fragment = _frag
        )
        shaders.append({"name": dir, "shader": _shdr})

    return shaders