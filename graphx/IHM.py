import pygame
from pygame import image

class IHM:
	class STATE:
		"""Represent a state of the ihm"""
		OPEN = 1
		CLOSE = 0

	class IMAGES:
		BASE = 0
		CIRCLE_BAR = 1
		CIRCLE_BUTTON = 2
		HORIZ_BAR = 3
		INPUT_VALUE = 4
		OPEN_IHM = 5

	"""This class allows to add some controls to the fractal"""
	def __init__(self, win_width, win_height, screen_surface):
		self.window_width = win_width
		self.window_height = win_height
		self.state = IHM.STATE.CLOSE
		self.sprites = [None for x in range(6)]
		self.screen = screen_surface
		self.load()

	def load(self):
		if not pygame.image.get_extended():
			print "[IHM] error: pygame does not support png loading"
			return
		self.sprites[IHM.IMAGES.BASE] = image.load('img/base-ihm.png').convert_alpha();
		self.sprites[IHM.IMAGES.CIRCLE_BAR] = image.load('img/circle-bar.png').convert_alpha();
		self.sprites[IHM.IMAGES.CIRCLE_BUTTON] = image.load('img/circle-button.png').convert_alpha();
		self.sprites[IHM.IMAGES.HORIZ_BAR] = image.load('img/horiz-bar.png').convert_alpha();
		self.sprites[IHM.IMAGES.INPUT_VALUE] = image.load('img/input-value.png').convert_alpha();
		self.sprites[IHM.IMAGES.OPEN_IHM] = image.load('img/open-ihm.png').convert_alpha();


	def draw(self):
		if self.state is IHM.STATE.CLOSE:
			self.screen.blit(self.sprites[IHM.IMAGES.BASE],
				(self.window_width - self.sprites[IHM.IMAGES.BASE].get_width(),
				self.window_height / 2 - self.sprites[IHM.IMAGES.BASE].get_height() / 2))
		else:
			pass

