import os
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

import pygame

"""
Loading images and put them into an 'Asset' object

AssetLoader
--
Loads assets according to directory structure


Asset
--
Sprite with properties: pygame.image, type, position

"""

class AssetType(Enum):
    Collider = "collider"
    PassThrough = "passthrough"
    Item = "item"
    Hazard = "hazard"
    Unknown = "unknown"

class AssetLoader():
    def __init__(self):
        ...


@dataclass
class Asset:
    image: pygame.image
    type: AssetType
    position: Tuple[int, int] = (0,0)

