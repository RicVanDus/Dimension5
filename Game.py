import pygame
from sys import exit

class Game:
    def __init__(self):
        pygame.init()

        screen_res = (800,600)
        self.running = True
        screen_flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(screen_res, screen_flags)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Dimension 5')

        # Background
        self.screen_bg = pygame.Surface(screen_res)
        self.screen_bg.fill('#111111')

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if pygame.K_ESCAPE:
                        self.running = False

            self.screen.blit(self.screen_bg,(0,0))

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        exit()

Game().run()