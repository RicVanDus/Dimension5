import pygame

"""
# Button for load
# Button for save
# Interface for choosing a tile
# Interface for putting in objects (off-grid)
# Level can't be saved if there's no player spawn

Small bar on top and bigger bar on the left for UI

Placing blocks: click and hold (painting)
Select objects

"""



SCREEN_RES = (2048, 1572)
INTERNAL_RES = (640, 480)
BG_COLOR = '#000000'
BG_UI_COLOR = '#222222'
BASE_FILE_PATH = 'levels/'

class LevelEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_RES)
        self.render_display = pygame.Surface(INTERNAL_RES)




    def run(self):
        ...


    def Export(self, data, filename) -> None:
        with open(file=BASE_FILE_PATH + filename) as file:
            file.write(data)

