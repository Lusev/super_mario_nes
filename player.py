from turtle import pos
import pygame as pg
from math import sin
from support import import_folder

class Player(pg.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        #print(self.animations)
        self.image = self.animations['idle_small'][self.frame_index]
 
        self.rect = self.image.get_rect(topleft = pos)
        
        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        
        # player movement
        self.speed = 1
        self.direction = pg.math.Vector2(0,0) # Vector2(x,y)
        self.gravity = 0.8
        self.jump_speed = -16
        self.heath_state = 1
                
        #player status
        self.status = 'idle'
        self.state = 'small'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.is_ducking = False
        
    def import_character_assets(self):
        character_path = r'./Assets/Graphics/mario/'
        self.animations = {'idle_small':[], 'run_small':[], 'jump_small':[], 'fall_small':[], 'idle_big': [], 'run_big': [], 'jump_big': [], 'fall_big': [], 'duck_big': [], 'idle_fire': [], 'run_fire': [], 'jump_fire': [], 'fall_fire': [], 'duck_fire': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            print(animation)
            self.animations[animation] = import_folder(full_path) # sends images to be appended in list.
    
    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('./Assets/Graphics/character/dust_particles/run/')
        
        
    def animate(self):
        animation = self.animations[self.status]
        
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else: 
            flipped_image = pg.transform.flip(image,True,False)
            self.image = flipped_image
            
        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
                self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
                self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
            
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            
            if self.facing_right:
                pos = self.rect.bottomleft - pg.math.Vector2(6,10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pg.math.Vector2(6,10)
                flipped_dust_particle = pg.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)
        
    def get_input(self, jump_sound):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else: 
            self.direction.x = 0
            
        if keys[pg.K_SPACE] and self.on_ground:
            jump_sound.play()
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            
        if keys[pg.K_DOWN] and (self.state == 'big' or self.state == 'fire'):
            print('here')
            self.is_ducking = True
        else:
            self.is_ducking = False
        
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump' + "_" + self.state 
        elif self.direction.y > 1:
            self.status = 'fall' + "_" + self.state 
        elif self.is_ducking and self.state != 'small':
            self.status = 'duck' + "_" + self.state 
        else:
            if self.direction.x != 0:
                self.status = 'run' + "_" + self.state 
            else:
                self.status = 'idle' + "_" + self.state 
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y  = self.jump_speed
        
    def change_state(self, state):
        self.state = state
         
    def update(self, jump_sound):
        self.get_input(jump_sound)
        self.get_status()
        self.animate()
        self.run_dust_animation()
        # self.wave_value()
        
