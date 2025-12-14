import os
import pygame

BASE_IMAGE_PATH = 'images/'


def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    return img

def load_images(path: str) -> list[pygame.Surface]:
    images = []
    for img_name in os.listdir(BASE_IMAGE_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images


class TweenFloat():
    """
        Tweens a float value in x seconds
    """

    def __init__(self, start_value: float, end_value: float, time: float):
        self.start_value = start_value
        self.value = start_value
        self.end_value = end_value
        self.time = time

    def go(self) -> float:
        running = True
        while running:
            # still have to cap value to end up with exactly the end valueS
            if self.value != self.end_value:
                self.value += ((self.end_value - self.start_value) / (60.0 * self.time))
                return self.value
            else:
                running = False