import pygame, sys, random
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile, MovingPlatform
from player import Player
from pygame.math import Vector2 as vector
from bullet import Bullet, FireAnimation
from enemy import Enemy

print("\033[43m main \033[0m")

class All_sprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        
        # sky
        self.fg_sky = pygame.image.load('../graphics/sky/fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load('../graphics/sky/bg_sky.png').convert_alpha()
        tmx_map = load_pygame('../data/map.tmx')
        
        # dmensions
        self.sky_width = self.bg_sky.get_width()
        self.padding = WINDOW_WIDTH / 2
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = int(map_width // self.sky_width)

    def custom_draw(self, player):
       
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2
        
        for x in range(self.sky_num):
            self.bg_sky_rect = self.bg_sky.get_rect(center = (x*self.sky_width-self.padding, 800))
            self.bg_sky_rect.center -= self.offset/10
            self.display_surface.blit(self.bg_sky, self.bg_sky_rect)
            
        for x in range(self.sky_num):
            self.fg_sky_rect = self.fg_sky.get_rect(center = (x*self.sky_width-self.padding, 1000))
            self.fg_sky_rect.center -= self.offset/5
            self.display_surface.blit(self.fg_sky, self.fg_sky_rect)
        
        # blit all sprites
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    
# ============================================================================ #
# MAIN
# ============================================================================ #

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Contra')
        self.clock = pygame.time.Clock()
        
        # groups
        self.all_sprites = All_sprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()
        
                 
        self.setup()
        
        # bullet images
        self.bullet_surf = pygame.image.load('../graphics/bullet.png').convert_alpha()
        self.fire_surf = [
            pygame.image.load('../graphics/fire/0.png').convert_alpha(),
            pygame.image.load('../graphics/fire/1.png').convert_alpha()
            ]
        
        self.ready_to_shoot = True
        self.shoot_time = 0
        self.cooldown = 150
        
        # self.music = pygame.mixer.Sound('../sound/music.mp3')
        # self.music.set_volume(0.1)
        # self.music.play(-1)
        
        self.sound_shoot = pygame.mixer.Sound('../sound/bullet.wav')
        self.sound_shoot.set_volume(0.1)
        self.sound_bullet_hit_1 = pygame.mixer.Sound('../sound/metal-hit-1.mp3')
        self.sound_bullet_hit_2 = pygame.mixer.Sound('../sound/metal-hit-2.mp3')
        self.sound_bullet_hit_3 = pygame.mixer.Sound('../sound/metal-hit-3.mp3')
        self.sound_bullet_hit_4 = pygame.mixer.Sound('../sound/metal-hit-4.mp3')
        self.sound_bullet_hit_1.set_volume(0.05)
        self.sound_bullet_hit_2.set_volume(0.05)
        self.sound_bullet_hit_3.set_volume(0.05)
        self.sound_bullet_hit_4.set_volume(0.05)
        

        
    def setup(self):
# ============================================================================ #
#  SETUP
# ============================================================================ #
        tmx_map = load_pygame('../data/map.tmx')
        
        # tiles (level to collide with)
        for x, y, surf in  tmx_map.get_layer_by_name('Level').tiles():
           CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprites])    
        
        # tiles
        layers = ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']
        for layer_name in layers: 
            for x, y, surf in  tmx_map.get_layer_by_name(layer_name).tiles():
                Tile((x * 64, y * 64), surf, self.all_sprites, LAYERS[layer_name])

        # Objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                self.player = Player(
                    pos = (obj.x,obj.y),
                    groups = [self.all_sprites,self.vulnerable_sprites],
                    path = '../graphics/player',
                    collision_sprites = self.collision_sprites,
                    shoot = self.shoot)
            if obj.name == 'Enemy':
                Enemy(
                    pos = (obj.x, obj.y),
                    path = '../graphics/enemy',
                    groups = [self.all_sprites,self.vulnerable_sprites],
                    shoot = self.shoot,
                    player =  self.player,
                    collision_sprites = self.collision_sprites)

        # Platforms
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == "Platform":
                MovingPlatform((obj.x,obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites])
            else: # border
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)
                
        

    def platform_collisions(self):
# ============================================================================ #
# Platform collisions
# ============================================================================ #
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                # bounce platform
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0: # up
                        platform.rect.top =  border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom =  border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
                         
    def bullet_collisions(self):
        
            hit = pygame.sprite.pygame.sprite.groupcollide(self.collision_sprites, self.bullet_sprites, False, True)
            if len(hit) > 0:
                sound_number = random.randint(1, 4)
                eval(f"self.sound_bullet_hit_{sound_number}.play()")
            
            # enemies
            for sprite in self.vulnerable_sprites.sprites():
                if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True):
                    sprite.health -= 1
                    print("health -1, zostalo:", sprite.health)
                    if sprite.health <= 0:
                        sprite.kill()
                    

# ============================================================================ #
#   SHOOT
# ============================================================================ #
    def shoot(self, pos, direction, entity):
        self.shoot_timer()
        
        if self.ready_to_shoot:
            Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprites])
            self.sound_shoot.play() 
            self.ready_to_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
            FireAnimation(entity, self.fire_surf, direction, self.all_sprites)
        
    def shoot_timer(self):
        current_time = pygame.time.get_ticks()
        # print(current_time, self.shoot_time)
        if current_time - self.shoot_time > self.cooldown:
            self.ready_to_shoot = True
     
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            dt = self.clock.tick() / 1000
            self.display_surface.fill((249,131,103))
            # self.display_surface.fill((37, 41, 47))
            
            self.platform_collisions()
            # update
            self.all_sprites.update(dt)
            self.bullet_collisions()
            # self.all_sprites.draw(self.display_surface)
            self.all_sprites.custom_draw(self.player)
            
            pygame.display.update()
        
if __name__  == '__main__':
    main = Main()
    main.run()

