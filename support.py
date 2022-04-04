from os import walk
import pygame as pg
from csv import reader
from settings import tile_size

def import_folder(path):
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def import_csv_layout(path):
    background_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            background_map.append(list(row))
        return background_map
    
def import_cut_graphics(path):
    surface = pg.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pg.Surface((tile_size, tile_size), flags = pg.SRCALPHA) #16 by 16
            new_surf.blit(surface, (0,0), pg.Rect(x, y , tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles
