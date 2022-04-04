import pygame as pg

class Score_Display:
    def __init__(self, surface):
        
        # setup 
        self.display_surface = surface
        
        #coins
        self.coin = pg.image.load('./Assets/Graphics/coin/coin_0.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (80,10))
        self.font = pg.font.Font('C:/Users/edgar/AppData/Local/Microsoft/Windows/Fonts/SuperPlumberBrothers.ttf', 14)
        
        #game over Mario
        self.mario_gameover = pg.image.load('./Assets/Graphics/mario/idle_small/1.png').convert_alpha()
        self.mario_gameover_rect = pg.Rect(225,120,10,10)
        # score
        self.score = 0
        self.coins = 0
        self.lives = 3
        self.time = 500
        self.go_time = 5
        
        # Timers
        self.start_timer = 0
        self.gameover_timer = 0
        
        self.game_state = 'running'
        
     
    def set_lives(self, lives):
        self.lives += lives   
    def set_score(self, score):
         self.score += score
    def set_coins(self):
        self.coins += 1
        
    def display_hud(self):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(self.coins),False,'#FFFFFF')
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.right +4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)
        
        name_surf = self.font.render('MARIO', False, '#FFFFFF')
        name_rect = pg.Rect(5,5,10,10)
        
        score_amount_surf = self.font.render(str(self.score), False, '#FFFFFF')
        score_amount_rect = pg.Rect(5,20,10,10)
        
        world_surf = self.font.render("WORLD", False, '#FFFFFF')
        world_rect = pg.Rect(300,5,10,10)
        
        world_level_surf = self.font.render("1-1", False, '#FFFFFF')
        world_level_rect = pg.Rect(307,25,10,10)

        time_surf = self.font.render("TIME", False, '#FFFFFF')
        time_rect = pg.Rect(407,5,10,10)
        
        count_down_surf = self.font.render(str(self.time), False, '#FFFFFF')
        count_down_rect = pg.Rect(407,25,10,10)
        
        current_time = int(pg.time.get_ticks())

        
        if current_time - self.start_timer >= 1000:
            self.time -= 1
            self.start_timer = int(current_time)
        
        self.display_surface.blit(name_surf, name_rect)
        
        self.display_surface.blit(score_amount_surf, score_amount_rect)
        
        self.display_surface.blit(world_surf, world_rect)

        self.display_surface.blit(world_level_surf, world_level_rect)
    
        self.display_surface.blit(time_surf, time_rect)
        
        self.display_surface.blit(count_down_surf, count_down_rect)

        
    def display_gameover(self, is_gameover):
        current_time = int(pg.time.get_ticks())
        if current_time - self.gameover_timer >= 1000:
            self.go_time -= 1
            self.gameover_timer = int(current_time)
            
        
            
        self.display_surface.fill((0,0,0))
        self.display_hud()
        gameover_surf = self.font.render("GAME OVER", False, '#FFFFFF')
        gameover_rect = pg.Rect(225,120,10,10)
       # self.display_surface.blit(gameover_surf, gameover_rect)
       
        lives_surf = self.font.render(" x "+str(self.lives), False, '#FFFFFF')
        lives_rect = pg.Rect(250, 120, 10,10)
        
        gameover_surf = self.font.render("GAME OVER", False, '#FFFFFF')
        gameover_rect = pg.Rect(225,120,10,10)

        if is_gameover:
            self.display_surface.blit(gameover_surf, gameover_rect)
        else:
            self.display_surface.blit(self.mario_gameover, self.mario_gameover_rect)
            self.display_surface.blit(lives_surf, lives_rect)    
            
        if self.go_time <= 0:      
            self.go_time = 5
            self.game_state = 'running'