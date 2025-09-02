import pygame


# for any animations, where you swap out images at a certain rate
class Animation():
    def __init__(self, images, frametime: int, loop: bool):
        self.images = images
        self.frametime = frametime
        self.loop = loop

        self.frame = 0


    def play(self) -> pygame.Surface:
        while True:
            self.frame += 1
            return self.images[int(self.frame / self.frametime % len((self.images)))]


    def pause(self):
        ...
