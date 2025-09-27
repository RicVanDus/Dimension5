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
        self.dir_force = [0.0, 0.0]

        self.move_speed = 0.6
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.moving_down = False
        self.facing_right = True
        self.velocity = [0.0, 0.0]

        self.collided_dir = {'left': False, 'right': False, 'top': False, 'bottom': False}

    def rect(self) -> pygame.Rect:
        return pygame.Rect((self.pos[0], self.pos[1]), (self.size[0], self.size[1]))

    def update(self):
        if self.selected:
            frame_movement = (self.dir_force[0] + ((self.moving_right - self.moving_left) * self.move_speed), self.dir_force[1])

            player_rect = self.rect()
            self.pos[1] += frame_movement[1]
            for rect in self.game.selected_tilemap.physics_tiles_around(self.pos):
                if player_rect.colliderect(rect):
                    if self.moving_left:
                        player_rect.left = rect.right
                    if self.moving_right:
                        player_rect.right = rect.left
                    self.pos[0] = player_rect.x

            player_rect = self.rect()
            self.pos[0] += frame_movement[0]
            # collision with tiles
            for rect in self.game.selected_tilemap.physics_tiles_around(self.pos):
                print(player_rect.centerx, "  ", rect.centerx)
                if player_rect.colliderect(rect):
                    if self.dir_force[1] > 0:
                        player_rect.bottom = rect.top
                        self.pos[1] = player_rect.y
                        self.dir_force[1] = 0
                    if self.dir_force[1] < 0:
                        player_rect.top = rect.bottom
                        self.pos[1] = player_rect.y


            self.dir_force[1] = min(1.5, self.dir_force[1] + 0.05)

        if self.jump:
            self.dir_force[1] = -1


    def select_player(self):
        self.selected = True

    def deselect_player(self):
        self.selected = False

    def render(self, surface, scroll_offset=[0,0]):
        surface.blit(self.player_image, (self.pos[0] - scroll_offset[0], self.pos[1] - scroll_offset[1]))
