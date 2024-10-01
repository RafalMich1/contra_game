import pygame, sys
from settings import *
from pygame.math import Vector2 as vector
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, shoot):
        super().__init__(pos, path, groups, shoot)
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'right'

        # collision
        self.collision_sprites = collision_sprites
        

        self.touch_top = False
        self.touch_bottom = False
        # vartical movement
        self.gravity = 15
        self.jump_speed = 1000
        self.on_floor = False
        self.duck = False
        
        self.health = 10
       
        self.sound_death = pygame.mixer.Sound('../sound/man-death-scream.mp3')
        self.sound_death.set_volume(0.3)


    
    def get_status(self):

        if self.direction.x == 0 and self.on_floor and not "_idle" in self.status:
            self.status = self.status.split('_')[0] + '_idle'        

        if self.direction != 0 and not self.on_floor:
            self.status = self.status.split('_')[0] + '_jump'
            
        if self.on_floor and self.duck and self.direction.x == 0:
            self.status = self.status.split('_')[0] + '_duck'    
            
    def check_contact(self):
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom      
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
      

        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
            if not keys[pygame.K_RIGHT]: self.can_jump = True
            
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
            if not keys[pygame.K_LEFT]: self.can_jump = True
            
        else:
            self.direction.x = 0   
            
        if keys[pygame.K_UP] and self.on_floor == True and self.can_jump == True:
            self.on_floor = False
            self.direction.y = -self.jump_speed
            self.can_jump = False
            
        if keys[pygame.K_DOWN]:
            self.duck = True
            self.can_jump = True
        else:
            self.duck = False
            
        if keys[pygame.K_SPACE]:
            direction = vector(1,0) if self.status.split('_')[0] == 'right' else vector(-1,0)
            pos = self.rect.center + direction * 150
            y_offset = vector(10, -16) if not  "_duck" in self.status else vector(0, 10)
            self.shoot(pos + y_offset, direction, self)
            # print('shoot')
    
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                
                if direction == 'horizontal':
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x
                else:
                    # bottom collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                        # print('bottom collision')
                        self.touch_bottom = True
                    else:
                        self.touch_bottom = False
                        if '_jump' in self.status:
                             self.status = self.status.split('_')[0]

                    # top collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        # print('top collision')
                        self.touch_top = True
                    else:
                        self.touch_top = False
                        
                    self.pos.y = self.rect.y
                    self.direction.y = 0
                    
                    # print(self.touch_top, self.touch_bottom)
                    if not self.touch_top and not self.touch_bottom:
                        self.sound_death.play()
                        print("\033[43m Player Die \033[0m")
            
        if self.on_floor and self.direction.y != 0 :
            self.on_floor = False  

    def move(self, dt):
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        
        # vertical
        self.direction.y += self.gravity
        
        self.pos.y += self.direction.y * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')
                
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)















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