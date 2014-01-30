import sys
import math
import time
import random

from OpenGL.GLUT import *
from OpenGL.GL import *
import pygame
import pygame.locals

from graphx.Graphx import *
from turtle.Turtle import *
from lsystem import *
from Conf import Conf
from func import *

USED = [
	lambda t: FirstTree.FirstTree(t),
	lambda t: Tree2.Tree2(t),
	lambda t: Tree2.Tree2(t, -math.pi / 32),
	lambda t: Tree2.Tree2(t, -math.pi / 64),
	lambda t: Tree2.Tree2(t, +math.pi / 12),
	lambda t: Tree3.Tree3(t),
	lambda t: Tree3.Tree3(t, 0, -math.pi / 16),
	lambda t: Tree3.Tree3(t, 0, math.pi / 8),
	lambda t: Tree5.Tree5(t),
	lambda t: Tree5.Tree5(t,0, 0, 0.7),
	lambda t: Tree5.Tree5(t, 0, math.pi / 7, 0.7),
	lambda t: Tree6.Tree6(t, 1, 0),
	lambda t: Tree6.Tree6(t, 5, 0),
	lambda t: Tree6.Tree6(t, 3, 0),
]

class Main:
	"""Entry point"""
	def __init__(self):
		print "===== 3D L-system FOREST creator - call 'help' for usage information ==="
		if not 'help' in sys.argv:
			self.gx = Graphx()

		self.quit = False

		self.fractals = []
		self.turtles = []

		self.grid_prec = None
		self.fractal_prec = None
		self.grid_random = None
		self.debug = False


		self.parse_input()

		self.init_grid(self.grid_prec, self.grid_random)


	def parse_input(self):
		for arg in sys.argv:
			if ".py" in arg:
				continue
			if arg == "help":
				print Conf.FOREST_HELP
				exit()
			if arg == "debug":
				self.debug = True
			tmp = arg.split("=")
			if tmp[0] == "size":
				self.grid_prec = int(tmp[1])
			if tmp[0] == "fractal":
				self.fractal_prec = int(tmp[1])
			if tmp[0] == "random":
				self.grid_rangom = int(tmp[1])
			if tmp[0] == "debug":
				self.debug = True
				if len(tmp) > 1:
					if tmp[1] != "True":
						self.debug = False

		if not self.grid_prec or self.grid_prec < 1:
			self.grid_prec = 10
		if not self.fractal_prec:
			self.fractal_prec = -2
		if not self.grid_random:
			self.grid_random = 200.0 / (self.grid_prec - 2 if self.grid_prec > 2 else self.grid_prec)
		if self.grid_random <= 0:
			print "Error: random="+str(random)+": Cannot specify a random factor lower or equal to 0"
			exit()




	def init_grid(self, precision, rnd):
		if precision == 1:
			t = Turtle()
			self.turtles.append(t)
			self.fractals.append(USED[random.randint(0, len(USED) - 1)](t))
			return

		for x in xrange(precision):
			randx = random.random() * rnd
			randx -= randx / 2
			posx = -50.0 + x * 100.0 / (precision - 1) + randx
			for y in xrange(precision):
				randy = random.random() * rnd
				randy -= randy / 2
				posy = -50.0 + y * 100.0 / (precision - 1) + randy
				t = Turtle((posx, 0, posy))
				self.turtles.append(t)
				self.fractals.append(USED[random.randint(0, len(USED) - 1)](t))



	# The function called whenever a key is pressed
	# it propagates the events to the fractal and the graphx
	def event(self, e):
		if e.type == pygame.QUIT:
			self.quit = True
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				self.quit = True
			elif e.key == pygame.K_SPACE:
				self.follow_building = not self.follow_building;
		for f in xrange(len(self.fractals)):
			self.fractals[f].event(e)
		self.gx.event(e)

	def main(self):
		t_init = time.time()
		print "=============== Starting world generation, please wait... ==============="
		for f in xrange(len(self.fractals)):
			print "=============== Generation: [" + str(f) + "/" + str(len(self.fractals)) + "] " +  " ==============="
			self.fractals[f].setSteps(self.fractal_prec)
			self.fractals[f].generate()
		for f in xrange(len(self.fractals)):
			print "=============== Running turtle: [" + str(f) + "/" + str(len(self.fractals)) + "] " +  " ==============="
			self.fractals[f].runTurtleRun(stepbystep=('debug' in sys.argv))
		t_gen = time.time()
		print "=============== World generation successfully done !"
		print "=============== Generation time: ", (t_gen - t_init), 'sec'

		while not self.quit:
			for e in pygame.event.get():
				self.event(e)
			self.gx.clear()
			for f in xrange(len(self.fractals)):
				self.fractals[f].update()
				self.gx.setShader(self.fractals[f].getShader(), self.fractals[f].getUniforms())
				self.turtles[f].draw()
			self.gx.update()


Main().main()

