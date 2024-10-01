import pygame, sys
from settings import *
from pygame.math import Vector2 as vector

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(groups)
        
        if direction.x < 0:
            surf = pygame.transform.flip(surf, True, False)
        
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['Level']
        
        # move
        self.direction = direction
        self.bspeed = 1200
        self.pos = vector(self.rect.center)
        
        self.start_time = pygame.time.get_ticks()
        
    def update(self, dt):
        self.pos += self.direction * self.bspeed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        if pygame.time.get_ticks() - self.start_time > 1000:
            self.kill()
            
class FireAnimation(pygame.sprite.Sprite):
    def __init__(self, entity, surf_list, direction, groups):
        super().__init__(groups)
        self.entity = entity
        self.direction  = direction
        self.frames = surf_list
        if self.direction.x < 0:
            self.frames = [pygame.transform.flip(frame, True, False ) for frame in self.frames]
            
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = self.entity.rect.center)
        self.rect.x = self.rect.x + 55 * self.direction.x
        self.rect.y -= 15
        self.z = LAYERS['Level']

        
    def animate(self, dt):
        self.frame_index +=  15 * dt

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]  


        self.rect = self.image.get_rect(center = self.entity.rect.center)
        self.rect.x = self.rect.x + 55 * self.direction.x
        self.rect.y -= 15  if not "_duck" in self.entity.status else -10

    
    def update(self, dt):
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