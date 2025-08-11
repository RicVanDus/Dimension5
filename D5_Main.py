import pygame
from sys import exit

pygame.init()

screen_res = (800,600)
running = True
screen = pygame.display.set_mode(screen_res)
clock = pygame.time.Clock()

pygame.display.set_caption('Dimension 5')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()