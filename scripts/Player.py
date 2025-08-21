import pygame
import math

#Handles player movement
class Player:
    def __init__(self, game):
        self.game = game
        self.selected = True
        self.player_image = pygame.Surface((10,10))
        self.player_image.fill('white')
        self.pos = [50,50]
        self.velocity = [0,0]
        self.move_speed = 5
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.selected:
            self.player_controls()

    def player_controls(self):
        self.pos[0] += self.velocity[0] + ((self.moving_right - self.moving_left) * self.move_speed)
        # this can be removed asap.
        self.pos[0] = max(0, min(self.game.screen.get_width() - self.player_image.get_width(), self.pos[0]))

    def select_player(self):
        self.selected = True

    def deselect_player(self):
        self.selected = False

    def render(self, surface):
        surface.blit(self.player_image, self.pos)


