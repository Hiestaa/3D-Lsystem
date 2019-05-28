import math
import time

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

from Conf import Conf
from Vector import *

class Camera:
	"""Represent the camera"""
	def __init__(self, pos, look):
		self.pos = Vector((pos[0], pos[1], pos[2]))
		self.lookat = Vector((look[0], look[1], look[2]))
		self.angleY = 0
		self.angleX = 0
		self.angleZ = 0
		self.distance = 100
		gluLookAt(0.0, 0.0, 0.0,
					look[0], look[1], look[2],
					0.0, 1.0, 0.0)
		self.lookat = (0.0, 0.0, 0.0, time.time())
		pygame.key.set_repeat(500, 10)

	def update(self):
		self.angleY -= Conf.GRAPHX.CAMERA_ROTATION_VELOC
		pass

	# handle events
	def event(self, e):
		if e.type == pygame.KEYDOWN:
			if e.unicode == 'z':
				self.angleZ += 1
			if e.unicode == 's':
				self.angleZ -= 1
			if e.unicode == 'a':
				self.angleX += 1
			if e.unicode == 'e':
				self.angleX -= 1
			if e.unicode == 'q':
				self.angleY += 1
			if e.unicode == 'd':
				self.angleY -= 1
			if e.key == pygame.K_RETURN:
				self.angleX = 0
				self.angleZ = 0
				self.distance = 100
			if e.key == pygame.K_LEFT:
				Conf.GRAPHX.CAMERA_ROTATION_VELOC += 0.02
			elif e.key == pygame.K_RIGHT:
				Conf.GRAPHX.CAMERA_ROTATION_VELOC -= 0.02
		if e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 5:
				self.distance *= 1.1
			if e.button == 4:
				self.distance *= 0.9
		pass

	def look(self, lookat):
		# do not change the look at too fast: self.lookat[3] contains the time
		if time.time() - self.lookat[3] > Conf.GRAPHX.CAMERA_UPDATE_PERIOD or lookat is (0, 0, 0):
			self.lookat = (lookat[0], lookat[1], lookat[2], time.time())
		gluLookAt(self.lookat[0] + self.distance,self.lookat[1] + self.distance,self.lookat[2] + self.distance,
			self.lookat[0], self.lookat[1], self.lookat[2],
			0,1,0);
		glRotated(self.angleY,0,1,0);
		glRotated(self.angleX,1,0,0);
		glRotated(self.angleZ,0,0,1);


