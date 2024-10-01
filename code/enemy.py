import pygame, sys
from settings import *
from pygame.math import Vector2 as vector
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, path, groups, shoot, player, collision_sprites):
        super().__init__(pos, path, groups, shoot)
        self.player = player
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 1000
        
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top

    def get_status(self):
        if self.player.rect.centerx <= self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'
            
    def check_fire(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        
        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False
        
        if distance < 600 and same_y and  self.can_shoot:
            bullet_direction = vector(1,0) if self.status =='right' else vector(-1,0)
            
            y_offset = vector(0,-16)
            pos = self.rect.center + bullet_direction * 120
            self.shoot(pos + y_offset, bullet_direction,self)
            
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def shoot_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_time > self.cooldown:
            self.can_shoot = True    

    def update(self, dt):
        self.get_status()
        self.check_fire()
        self.animate(dt)
        
        self.shoot_timer()
        self.check_fire()












# ============================================================================ #
# LAUNCHER
# ============================================================================ #
import subprocess
def check_and_run_main():
    if "main" not in sys.modules:
        print("Main module not found, launching main.py...")
        
        print(f"\033[38;5;{196}m {'---------------------------------'} \033[0m")
        subprocess.run([sys.executable, "main.py"])
    else:
        print("Main module is already running.")
if __name__ == "__main__":
    check_and_run_main()