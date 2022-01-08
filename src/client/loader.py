#!/usr/bin/env python3
import json

from src.log import log, warn

POINTER = "resource_pointer.json"

assets = json.load(open(POINTER, "r"))

def init():
    pass

def getAsset(category, name):
    if len(assets) < 1:
        init()

    return assets[category][name]

def getAllFromCategory(category):
    _asts = []
    for obj in assets[category]:
        #log(f'Loading "{obj}" into memory. Metadata: <{assets[category][obj]}>', "Worker/AssetLoader")
        _asts.append(assets[category][obj])

    return _asts