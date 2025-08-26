import pygame
import math
from enum import Enum

# don't know if we need this
class PlayerState(Enum):
    DEAD = 1
    JUMPING = 2
    RUNNING = 3
    SHOOTING = 4


#Handles player movement
class Player:
    def __init__(self, game):
        self.game = game
        self.selected = True
        self.player_image = pygame.Surface((16,16))
        self.player_image.fill('white')
        self.pos = [50,50]
        self.size = [16,16]
        self.velocity = [0.0,0.0]

        self.move_speed = 0.6
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False


    def rect(self) -> pygame.Rect:
        return pygame.Rect((self.pos[0], self.pos[1]), (self.size[0], self.size[1]))


    def update(self):
        if self.selected:
            player_rect = self.rect()

            #check for collisions here: just a test with rects that are static. When we are moving to tilemaps, we can make this dynamic.
            if player_rect.colliderect(self.game.test_surface_rect):
                player_rect.bottom = self.game.test_surface_rect.top
                #self.pos[0] = player_rect.x
                self.pos[1] = player_rect.y
                print(self.pos)

            self.velocity[1] = min(1, self.velocity[1] + 0.02)
            self.player_controls()

    def player_controls(self):
        self.pos[0] += self.velocity[0] + ((self.moving_right - self.moving_left) * self.move_speed)
        self.pos[1] += self.velocity[1]

        # this can be removed asap.
        self.pos[0] = max(0, min(self.game.render_display.get_width() - self.player_image.get_width(), self.pos[0]))

        if self.moving_up:
            self.velocity[1] = -1


    def select_player(self):
        self.selected = True

    def deselect_player(self):
        self.selected = False

    def render(self, surface):
        surface.blit(self.player_image, self.pos)
