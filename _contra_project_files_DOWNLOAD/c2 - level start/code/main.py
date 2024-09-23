import pygame, sys
from settings import * 
from pytmx.util_pygame import load_pygame
from tile import Tile

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Contra')
		self.clock = pygame.time.Clock()

		# groups 
		self.all_sprites = pygame.sprite.Group()

		self.setup()

	def setup(self):
		tmx_map = load_pygame('../data/map.tmx')
		for x,y, surf in tmx_map.get_layer_by_name('Level').tiles():
			Tile((x * 0,y * 0), surf, self.all_sprites)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000
			self.display_surface.fill((249,131,103))

			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)

			pygame.display.update()

if __name__ == '__main__':
	main = Main()
	main.run()
