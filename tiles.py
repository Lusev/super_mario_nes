import pygame as pg
from support import import_folder
class Tile(pg.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))
        
    def update(self, x_shift):
        self.rect.x += x_shift
        
class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface
              
# class Koopas(StaticTile):
#     def __init__(self,size,x,y):
#         super().__init__(size,x,y,pg.image.load('./Assets/Graphics/enemy/koopa_troopa/walk/koopa_0.png').convert_alpha())
#         offset_y = y + size
#         self.rect = self.image.get_rect(bottomleft = (x,offset_y))
        
class AnimatedTile(Tile):
    def __init__(self, size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def update(self, shift):
        self.animate()
        self.rect.x += shift
        
class Goomba(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y
        self.rect = self.image.get_rect(center = (center_x,center_y))
        self.speed = 1
        
    def move(self):
        self.rect.x -= self.speed
    
    def reverse_image(self):
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        self.speed *= -1
    
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        
class Koopa(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y
        self.rect = self.image.get_rect(center = (center_x,center_y))
        self.speed = 1
        
    def move(self):
        self.rect.x -= self.speed
    
    def reverse_image(self):
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        self.speed *= -1
    
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        
class Mushroom(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y
        self.rect = self.image.get_rect(center = (center_x,center_y))
        self.speed = 1
        
    def move(self):
        self.rect.x -= self.speed
    
    def reverse_image(self):
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        self.speed *= -1
    
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        

class Fire(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y
        self.rect = self.image.get_rect(center = (center_x,center_y))
        self.speed = 0
        
    def move(self):
        self.rect.x -= self.speed
    
    def reverse_image(self):
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        self.speed *= 0
    
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        
class Coin(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y
        self.rect = self.image.get_rect(center = (center_x,center_y))

    
    
    def update(self, shift):
        self.rect.x += shift
        self.animate()
    