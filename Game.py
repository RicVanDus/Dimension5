import pygame
from scripts.Player import Player
from sys import exit

class Game:
    def __init__(self):
        pygame.init()

        screen_res = (640,480)
        self.running = True
        screen_flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(screen_res)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Dimension 5')

        # Background
        self.screen_bg = pygame.Surface(screen_res)
        self.screen_bg.fill('#222222')

        self.player1 = Player(self)

        self.selected_player = self.player1
        self.timer = 0

    def run(self):
        while self.running:
            self.timer += 1
            self.controls()

            self.screen.blit(self.screen_bg,(0,0))

            # maybe replace by a game manager? That manages the screens etc.
            self.player1.update()
            self.player1.render(self.screen)

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.selected_player.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.selected_player.moving_right = False


Game().run()