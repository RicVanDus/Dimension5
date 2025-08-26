import pygame

#maybe add biomes? So you can switch the look of the level
class Tilemap():
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

        for i in range(30):
            self.tilemap[str(i + 3) + ":100"] = {"type":"test", "pos":(i + 3, 100)}

    def render(self, surface):
        for loc in self.tilemap:
            ...