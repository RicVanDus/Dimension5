import pygame
import random

NEIGHBOR_OFFSETS = [(0, 0), (-1, 0), (-1, -1), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
PHYSICS_TILES = {'placeholder'}

#maybe add biomes? So you can switch the look of the level
class Tilemap():
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.tiles_off_grid = []

        for i in range(10):
            self.tilemap[str(i + 3) + ':10'] = {'type': 'placeholder', 'pos':(i + 3, 10)}

        for i in range(5):
            self.tilemap[str(i + 8) + ':9'] = {'type': 'placeholder', 'pos':(i + 8, 9)}

    def tiles_around(self, pos) -> list:
        tiles = []
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(offset[0] + tile_pos[0]) + ':' +  str(offset[1] + tile_pos[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_tiles_around(self, pos) -> list:
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect((tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size), (self.tile_size, self.tile_size)))
        return rects

    def render(self, surface, scroll_offset=[0,0]):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surface.blit(self.game.assets[tile['type']], (tile['pos'][0] * self.tile_size - scroll_offset[0],tile['pos'][1] * self.tile_size - scroll_offset[1]))