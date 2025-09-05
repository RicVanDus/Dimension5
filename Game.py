import pygame
from scripts.Player import Player
from scripts.Tilemap import Tilemap
from scripts.Utils import load_image, load_images
from sys import exit
import random

SCREEN_FLAGS = pygame.FULLSCREEN

class Game:
    def __init__(self):
        pygame.init()

        screen_res = (1024,786)
        internal_res = (640, 480)
        self.running = True

        self.screen = pygame.display.set_mode(screen_res)
        self.render_display = pygame.Surface(internal_res)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Dimension 5')

        self.player1 = Player(self)
        self.selected_player = self.player1
        self.timer = 0
        self.cam_scroll = [0,0]

        self.dim1_container = pygame.Surface((640,120))

        self.test_rect = pygame.Rect((30,30), (150,60))

        self.assets = {}
        self.load_assets()

        self.dim1_tilemap = Tilemap(self)
        self.selected_tilemap = self.dim1_tilemap


    def run(self):
        while self.running:
            self.timer += 1
            self.controls()


            self.cam_scroll[0] += (self.selected_player.rect().centerx - self.dim1_container.get_width() / 2 - self.cam_scroll[0]) / 30
            self.cam_scroll[1] += (self.selected_player.rect().centery - self.dim1_container.get_height() / 2 - self.cam_scroll[1]) / 30

            self.render_display.fill('#222222')

            pygame.draw.rect(self.render_display, (255,255,0,255),self.test_rect, 2, 8)

            #Temp here: we need a method for these containers
            self.dim1_container.fill('#012332')


            self.dim1_tilemap.render(self.dim1_container, self.cam_scroll)

            # maybe replace by a game manager? That manages the screens etc.
            self.player1.update()
            self.player1.render(self.dim1_container, self.cam_scroll)
            self.render_display.blit(self.dim1_container, (0, 180))
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.selected_player.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.selected_player.moving_right = False
                if event.key == pygame.K_UP:
                    self.selected_player.moving_up = False


    def load_assets(self):
        self.assets = {
            "placeholder" : load_image('test/placeholder.png')
        }

Game().run()