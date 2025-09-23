import pygame
import random

NEIGHBOUR_OFFSETS = [(0, 0), (-1, 0), (-1, -1), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
PHYSICS_TILES = {'placeholder', 'test/anim_placeholder'}

"""
    Tilemap
    -------
    Renders all static tiles.
    
    Need to be optimized: only render when in frame. 
"""
class Tilemap():
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.tiles_off_grid = []
        self.anim_objects = {} #need a way to clear this.

        for i in range(10):
            self.tilemap[((i + 3), 10)] = {'type': 'placeholder', 'pos':(i + 3, 10), 'anim': False}

        for i in range(5):
            self.tilemap[((i + 8), 9)] = {'type': 'test/anim_placeholder', 'pos':(i + 8, 9), 'anim': True}

    def tiles_around(self, pos) -> list:
        tiles = []
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOUR_OFFSETS:
            check_loc = ((offset[0] + tile_pos[0]), (offset[1] + tile_pos[1]))
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_tiles_around(self, pos) -> list:
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect((tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size), (self.tile_size, self.tile_size)))
        return rects

    #This renders animated objects only after being copied. using the same tilemap still has duplicate objects ofcourse.
    def render(self, surface, scroll_offset=[0,0]):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['anim']:
                if loc in self.anim_objects:
                    surface.blit(self.anim_objects[loc].play(), (tile['pos'][0] * self.tile_size - scroll_offset[0], tile['pos'][1] * self.tile_size - scroll_offset[1]))
                else:
                    self.anim_objects[loc] = self.game.assets[tile['type']].copy()
            else:
                surface.blit(self.game.assets[tile['type']], (tile['pos'][0] * self.tile_size - scroll_offset[0],tile['pos'][1] * self.tile_size - scroll_offset[1]))
