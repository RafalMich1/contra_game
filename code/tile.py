import pygame, sys
from settings import *
from pygame.math import Vector2 as vector

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        
class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups, LAYERS['Level'])
        self.old_rect = self.rect.copy()
    
class MovingPlatform(CollisionTile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        
        # float based movement
        self.direction = vector(0,1)
        self.speed = 120
        self.pos = vector(self.rect.topleft)
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))































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