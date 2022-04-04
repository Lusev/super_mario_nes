import pygame as pg
from pygame import mixer
from particles import ParticleEffect
from score_display import Score_Display
from tiles import Tile, StaticTile, Koopa, AnimatedTile, Goomba, Mushroom, Fire, Coin
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect
from support import import_csv_layout,import_cut_graphics

class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.world_shift = 0
        self.score_display = Score_Display(surface)
        self.level_data = level_data
        self.initialize()
        self.is_invisible =  False
        self.invisiblity_timer = 0
        self.i_timer = 3
        
        
        #audio
        pg.init()
        self.background_music = mixer.music.load('./Assets/Audio/background_music.ogg')
        mixer.music.play(-1)
        self.powerup_sound = mixer.Sound('./Assets/Audio/powerup.wav')
        self.coin_sound = mixer.Sound('./Assets/Audio/coin.wav')
        self.jump_sound = mixer.Sound('./Assets/Audio/jump.wav')
        self.fireball_sound = mixer.Sound('./Assets/Audio/fireball.wav')
        self.gameover_sound = mixer.Sound('./Assets/Audio/gameover.ogg')
        self.killed_sound = mixer.Sound('./Assets/Audio/killed.ogg')
        self.stomp_sound = mixer.Sound('./Assets/Audio/stomp.wav')
        self.bump_sound = mixer.Sound('./Assets/Audio/bump.wav')
        self.kick_sound = mixer.Sound('./Assets/Audio/kick.wav')
        self.shrink_sound = mixer.Sound('./Assets/Audio/shrink.wav')
        self.play_music = True
        
        
    def check_invisiblity(self):
        
        if self.is_invisible == True:     
            current_time = int(pg.time.get_ticks())
              
            if current_time - self.invisiblity_timer >= 1000:
                self.i_timer -=1
                self.invisiblity_timer = int(current_time)
                
                if self.i_timer <= 0:      
                    self.i_timer = 3
                    self.is_invisible = False
        
    def initialize(self):
        
        # mario 
        player_layout = import_csv_layout(self.level_data['mario'])
    
        self.player = pg.sprite.GroupSingle()
        self.start = pg.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        # dust
        self.dust_sprite = pg.sprite.GroupSingle()
    
        #ground setup
        ground_layout = import_csv_layout(self.level_data['ground'])
        self.ground_sprites = self.create_tile_group(ground_layout, 'ground')
     
        #red_bricks setup
        red_brick_layout = import_csv_layout(self.level_data['red_bricks'])
        self.red_brick_sprites = self.create_tile_group(red_brick_layout, 'red_bricks')
        
        #coin_blockslayout
        coin_blocks_layout = import_csv_layout(self.level_data['coins_blocks'])
        self.coin_blocks_sprites = self.create_tile_group(coin_blocks_layout, 'coins_blocks')
        
        #coins
        coins_layout = import_csv_layout(self.level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')
        
        #stair_blockslayout
        stair_blocks_layout = import_csv_layout(self.level_data['stair_blocks'])
        self.stair_blocks_sprites = self.create_tile_group(stair_blocks_layout, 'stair_blocks')
        
        #pipes_layout
        pipes_layout = import_csv_layout(self.level_data['pipes'])
        self.pipes_sprites = self.create_tile_group(pipes_layout, 'pipes')
               
        # goomba
        goomba_layout = import_csv_layout(self.level_data['goombas'])
        self.goomba_sprites = self.create_tile_group(goomba_layout, 'goombas')
        
        # koopa
        koopa_layout = import_csv_layout(self.level_data['koopas'])
        self.koopa_sprites = self.create_tile_group(koopa_layout, 'koopas')
        
        #item_block
        item_block_layout = import_csv_layout(self.level_data['item_blocks'])
        self.item_blocks_sprites = self.create_tile_group(item_block_layout, 'item_blocks')
        
        #mushroom
        mushroom_layout = import_csv_layout(self.level_data['mushroom'])
        self.mushroom_sprites = self.create_tile_group(mushroom_layout, 'mushroom')
        
        #fire_flower
        fire_layout = import_csv_layout(self.level_data['fire'])
        self.fire_sprites = self.create_tile_group(fire_layout, 'fire')
        
        #constraints
        constraint_block_layout = import_csv_layout(self.level_data['constraint_block'])
        self.constraint_block_sprites = self.create_tile_group(constraint_block_layout, 'constraint_block')
        
        #jump points
        self.jump_points_sprite = pg.sprite.Group()
        
    def clear(self):
        self.goomba_sprites.empty()
        self.player.empty()
    
    def create_tile_group(self, layout, type):
        sprite_group = pg.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    
                    x =  col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'ground':
                        ground_tile_list = import_cut_graphics('./Assets/Graphics/ground/Ground_Brick.png')
                        tile_surface = ground_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y,tile_surface)
                    if type == 'red_bricks':
                        red_brick_tile_list = import_cut_graphics('./Assets/Graphics/red_brick/Red_Brick.png')
                        tile_surface = red_brick_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'coins_blocks':
                        red_brick_tile_list = import_cut_graphics('./Assets/Graphics/coin_block/Coin_Block.png')
                        tile_surface = red_brick_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    if type == 'stair_blocks':
                        stair_block_tile_list = import_cut_graphics('./Assets/Graphics/stair_block/Stair_Blocks.png')
                        tile_surface = stair_block_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    if type == 'pipes':
                        pipe_tile_list = import_cut_graphics('./Assets/Graphics/pipes/pipe_small.png')
                        tile_surface = pipe_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'mushroom':
                        sprite = Mushroom(tile_size, x, y, './Assets/Graphics/mushroom')   

                    if type == 'coins':
                        sprite = Coin(tile_size, x, y, './Assets/Graphics/coin')  
                        
                    if type == 'fire':
                        sprite = Fire(tile_size, x, y, './Assets/Graphics/fire')
                    
                    if type == 'goombas':
                        sprite = Goomba(tile_size,x,y,'./Assets/Graphics/enemy/goomba/walk')

                    if type == 'koopas':

                        sprite = Koopa(tile_size,x,y,'./Assets/Graphics/enemy/koopa_troopa/walk')
                        
                    if type == 'item_blocks':
                        sprite = AnimatedTile(tile_size, x, y, './Assets/Graphics/item_block')
                        
                    if type == 'constraint_block':
                        sprite = Tile(tile_size, x, y)
                        
                    if type == 'coin':
                        if val == '0': sprite = StaticTile(tile_size, x,y, './Assets/Graphics/coin/coin_0.png')  
                        
                    sprite_group.add(sprite)

        return sprite_group
           
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x =  col_index * tile_size
                y = row_index * tile_size
                if val == '1':
                    sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                    
                if val == '0':
                    mario_surface = pg.image.load('./Assets/Graphics/mario/mario_left_back_3.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, mario_surface)
                    self.start.add(sprite)
    
    
    def minions_collision(self):
        for minion in self.goomba_sprites.sprites():
            if pg.sprite.spritecollide(minion, self.constraint_block_sprites, False):
                minion.reverse()
        
        
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pg.math.Vector2(10, 5)
        else: 
            pos += pg.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)
                
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < screen_width - (screen_width -1) and direction_x < 0:
            self.world_shift = 0
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else: 
            self.world_shift = 0
            player.speed = 3
            
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        collidable_sprites = self.ground_sprites.sprites() + self.coin_blocks_sprites.sprites() + self.stair_blocks_sprites.sprites() + self.pipes_sprites.sprites() + self.red_brick_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
                    
    def verticle_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        collidable_sprites = self.ground_sprites.sprites() + self.coin_blocks_sprites.sprites() + self.stair_blocks_sprites.sprites() + self.pipes_sprites.sprites() + self.red_brick_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
            self.bump_sound.play()
    
    def check_enemy_collisions(self):
        enemy_collisions = pg.sprite.spritecollide(self.player.sprite,self.goomba_sprites, False)
        
        if enemy_collisions:
            for enemy in enemy_collisions: 
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >=0:
                    self.player.sprite.direction.y = -15
                    self.stomp_sound.play()
                    jump_points_sprite = ParticleEffect(enemy.rect.center,'points')
                    self.jump_points_sprite.add(jump_points_sprite)
                    self.score_display.set_score(100)
                    enemy.kill()
                    
                else:
                    for player in self.player.sprites():
                        if self.is_invisible == False:
                            self.is_invisible = True
                            if player.state == 'fire':
                                player.change_state('big')
                                self.shrink_sound.play()
                            elif player.state == 'big':
                                player.change_state('small')
                                self.shrink_sound.play()
                            elif player.state == 'small':
                                self.score_display.set_lives(-1)
                                if self.score_display.lives < 0: 
                                    self.score_display.game_state = 'gameover'
                                    self.play_music =  False
                                else:
                                    self.score_display.game_state = 'death'
                                    self.killed_sound.play()
                                    self.play_music =  False
   
                    #self.player.sprite.get_damage()
        
    def check_collectable_collision(self, sprite_list, collectable_type):
        collectable_collision = pg.sprite.spritecollide(self.player.sprite, sprite_list, False)
        
        if collectable_collision: 
            for collectable in collectable_collision:
                for player in self.player.sprites():
                    if collectable_type == 'mushroom':
                        self.powerup_sound.play()
                        self.score_display.set_score(50)
                        if player.state == 'small':
                            player.change_state('big')
                    elif collectable_type == 'fire':
                        self.score_display.set_score(100)
                        player.change_state('fire')
                        self.powerup_sound.play()
                    elif collectable_type == 'coin':
                        self.score_display.set_score(10)
                        self.score_display.set_coins()
                        self.coin_sound.play()
                collectable.kill()
            
        
    def run(self):
        if self.score_display.game_state == 'gameover':
            if self.play_music:
                pg.mixer.music.pause()            
            self.score_display.display_gameover(True)
            self.clear()
            self.initialize()
              
        elif self.score_display.game_state == 'death':
            if self.play_music:
                pg.mixer.music.pause()
            self.clear()
            self.initialize()
            self.score_display.display_gameover(False)
        elif self.score_display.game_state == 'running':
            if self.play_music == False:
                pg.mixer.music.unpause()

            self.ground_sprites.draw(self.display_surface)
            self.ground_sprites.update(self.world_shift)
            
            self.red_brick_sprites.update(self.world_shift)
            self.red_brick_sprites.draw(self.display_surface)
            
            self.coin_blocks_sprites.update(self.world_shift)
            self.coin_blocks_sprites.draw(self.display_surface)

            self.coins_sprites.update(self.world_shift)
            self.coins_sprites.draw(self.display_surface)
            
            self.stair_blocks_sprites.update(self.world_shift)
            self.stair_blocks_sprites.draw(self.display_surface)
            
            self.pipes_sprites.draw(self.display_surface)
            self.pipes_sprites.update(self.world_shift)
            
            self.constraint_block_sprites.update(self.world_shift)
            self.minions_collision()
            self.goomba_sprites.draw(self.display_surface)
            self.goomba_sprites.update(self.world_shift)
            self.jump_points_sprite.update(self.world_shift)
            self.jump_points_sprite.draw(self.display_surface)
            
            self.koopa_sprites.draw(self.display_surface)
            self.koopa_sprites.update(self.world_shift)
            
            
            # item blocks
            self.item_blocks_sprites.update(self.world_shift)
            self.item_blocks_sprites.draw(self.display_surface)
            
            # mushroom
            self.mushroom_sprites.update(self.world_shift)
            self.mushroom_sprites.draw(self.display_surface)

            # fire
            self.fire_sprites.update(self.world_shift)
            self.fire_sprites.draw(self.display_surface)
            
            # mario sprite
            self.start.update(self.world_shift)
            self.start.draw(self.display_surface)
            
            
            #dust particles
            self.dust_sprite.update(self.world_shift)
            self.dust_sprite.draw(self.display_surface)
            
            self.scroll_x()
            
            self.score_display.display_hud()
    
            # player
            self.player.update(self.jump_sound)
            self.horizontal_movement_collision()
            self.verticle_movement_collision()
            self.player.draw(self.display_surface)
            
            #self.change_coin_collisions()
            self.check_enemy_collisions()
            self.check_collectable_collision(self.mushroom_sprites, 'mushroom')
            self.check_collectable_collision(self.fire_sprites, 'fire')
            self.check_collectable_collision(self.coins_sprites, 'coin')
            self.check_invisiblity()