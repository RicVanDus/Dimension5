import pygame

from scripts.Animation import Animation
from scripts.Player import Player
from scripts.Tilemap import Tilemap
from scripts.Utils import load_image, load_images
from sys import exit
import random

SCREEN_FLAGS = pygame.FULLSCREEN
SCREEN_RES = (1024, 786)
INTERNAL_RES = (640, 480)


class Game:
    def __init__(self):
        pygame.init()


        self.running = True

        self.screen = pygame.display.set_mode(SCREEN_RES)
        self.render_display = pygame.Surface(INTERNAL_RES)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Dimension 5')

        self.player1 = Player(self)
        self.selected_player = self.player1
        self.timer = 0

        self.dim1_cam_scroll = [0, 0]
        self.dim2_cam_scroll = [0, 0]
        self.dim3_cam_scroll = [0, 0]
        self.dim4_cam_scroll = [0, 0]

        self.dim_cam_scrolls = [
            self.dim1_cam_scroll,
            self.dim2_cam_scroll,
            self.dim3_cam_scroll,
            self.dim4_cam_scroll
        ]

        self.dim1_container = pygame.Surface((640, 120), pygame.SRCALPHA)
        self.dim2_container = pygame.Surface((640, 120), pygame.SRCALPHA)
        self.dim3_container = pygame.Surface((640, 120), pygame.SRCALPHA)
        self.dim4_container = pygame.Surface((640, 120), pygame.SRCALPHA)

        self.dim_containers = [
            self.dim1_container,
            self.dim2_container,
            self.dim3_container,
            self.dim4_container
            ]

        self.dim1_gameview = pygame.Surface((600, 100))
        self.dim2_gameview = pygame.Surface((600, 100))
        self.dim3_gameview = pygame.Surface((600, 100))
        self.dim4_gameview = pygame.Surface((600, 100))

        self.dim_gameviews = [
            self.dim1_gameview,
            self.dim2_gameview,
            self.dim3_gameview,
            self.dim4_gameview
        ]

        self.assets = {}
        self.load_assets()

        self.dim1_tilemap = Tilemap(self)
        self.selected_tilemap = self.dim1_tilemap

        self.dimensions_active = 1
        self.active_dimension = 0
        self.current_level = 1

        self.press_down = False



    def run(self):
        while self.running:
            self.timer += 1
            self.controls()

            self.dim1_cam_scroll[0] += (self.selected_player.rect().centerx - self.dim1_gameview.get_width() / 2 - self.dim1_cam_scroll[0]) / 30
            self.dim1_cam_scroll[1] += (self.selected_player.rect().centery - self.dim1_gameview.get_height() / 2 - self.dim1_cam_scroll[1]) / 30

            self.render_display.fill('#222222')

            self.render_gameplay()

            self.screen.blit(pygame.transform.scale(self.render_display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        exit()

    # contains ALL controls
    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # quit
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # player controls
                if event.key == pygame.K_LEFT:
                    self.selected_player.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.selected_player.moving_right = True
                if event.key == pygame.K_UP:
                    self.selected_player.moving_up = True
                if event.key == pygame.K_DOWN and self.press_down == False:
                    self.dimensions_active += 1
                    if self.dimensions_active >= 5:
                        self.dimensions_active = 1
                    self.press_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.selected_player.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.selected_player.moving_right = False
                if event.key == pygame.K_UP:
                    self.selected_player.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.press_down = False


    def render_gameplay(self):
        for i in range(self.dimensions_active):
            self.render_dim_screen(i)


    def render_dim_screen(self, dimension):
        self.dim_containers[dimension].fill('#222222')
        self.dim_gameviews[dimension].fill('#233200')
        self.dim1_tilemap.render(self.dim_gameviews[dimension], self.dim1_cam_scroll)

        #need to make this dynamic still
        if dimension == self.active_dimension:
            self.player1.update()
            self.player1.render(self.dim1_gameview, self.dim1_cam_scroll)

        self.dim_containers[dimension].blit(self.dim_gameviews[dimension], (30, 15))

        rect = self.dim_gameviews[dimension].get_rect()
        rect.x += 30
        rect.y += 15
        pygame.draw.rect(self.dim_containers[dimension], (255, 255, 255, 255), rect, 2, 8)

        # calculating position
        container_height_offset = self.dim_containers[dimension].get_height() / 2
        container_pos = (INTERNAL_RES[1] / 2) - (container_height_offset * (self.dimensions_active - dimension)) + (container_height_offset * dimension)
        self.render_display.blit(self.dim_containers[dimension], (0, container_pos))


    def select_next_dimension(self):
        ...


    def load_assets(self):
        self.assets = {
            "placeholder" : load_image('test/placeholder.png'),
            "test/anim_placeholder" : Animation(load_images('test'), 100, True)
        }



Game().run()