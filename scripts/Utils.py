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

