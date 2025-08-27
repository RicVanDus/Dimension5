import pygame
import random

#maybe add biomes? So you can switch the look of the level
class Tilemap():
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

        for i in range(30):
            if random.randint(0,1) > 0:
                self.tilemap[str(i + 3) + ':10'] = {'type': 'placeholder', 'pos':(i + 3, 10)}

    def render(self, surface, scroll_offset=[0,0]):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surface.blit(self.game.assets[tile['type']], (tile['pos'][0] * self.tile_size - scroll_offset[0],tile['pos'][1] * self.tile_size - scroll_offset[1]))