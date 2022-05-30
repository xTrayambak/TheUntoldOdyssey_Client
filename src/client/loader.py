#!/usr/bin/env python3
"""
Asset locator. Locates the destination for assets inside resource_pointer.json
"""
import json
from pathlib import Path

from src.log import log, warn

POINTER = f"resource_pointer.json"

assets = json.load(open(POINTER, "r"))

def getAsset(category, name):
    """
    Get a particular asset of name `name` from category `category`.
    """

    return assets[category][name]

def getAllFromCategory(category):
    """
    Get all assets from a particular category.
    """
    _asts = []
    for obj in assets[category]:
        _asts.append(assets[category][obj])

    return _asts