import pygame


# for any animations, where you swap out images at a certain rate
# make sure frametime is based on 60 fps !!!!!!!!!

class Animation():
    def __init__(self, images, frametime: int, loop: bool):
        self.images = images
        self.frametime = frametime
        self.loop = loop

        self.frame = 0

    def copy(self):
        return Animation(self.images, self.frametime, self.loop)

    def play(self) -> pygame.Surface:
        while True:
            self.frame += 1
            return self.images[int(self.frame / self.frametime % len(self.images))]


    def pause(self):
        ...
