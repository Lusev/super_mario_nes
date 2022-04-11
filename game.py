import pygame as pg, sys
from settings import *
from tiles import Tile
from level import Level
from game_data import level_0
from score_display import Score_Display

pg.init()
screen_width = 500
screen_height = 239
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()
level_01 = Level(level_0, screen)
bg = pg.image.load('./Assets/Graphics/background/level_bg_fixed.png').convert_alpha()

# game ui
coins = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill('#acc8fc')
    screen.blit(bg,(0,0))
    
    level_01.run()

    pg.display.update()
    clock.tick(60)