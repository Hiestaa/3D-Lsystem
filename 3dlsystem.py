import sys
import math
import time

from OpenGL.GLUT import *
from OpenGL.GL import *
import pygame
import pygame.locals

from graphx.Graphx import *
from turtle.Turtle import *
from lsystem import *
from Conf import Conf
from func import *

# command line arguments
ARGUMENTS = {
	'tree1': 	lambda t: FirstTree.FirstTree(t),
	'tree2': 	lambda t: Tree2.Tree2(t),
	'tree2D':	lambda t: Tree2D.Tree2D(t),
	'tree3':	lambda t: Tree3.Tree3(t),
	'tree4':	lambda t: Tree4.Tree4(t),
	'tree3psy':	lambda t: Tree3psy.Tree3psy(t),
	'hilbert':	lambda t: HilbertCurve.HilbertCurve(t),
	'hilbert3D':lambda t: HilbertCurve3D.HilbertCurve3D(t),
	'koch':		lambda t: KochCurve.KochCurve(t),
	'dragon':	lambda t: Dragon.Dragon(t),
	'tedragon':	lambda t: Tedragon.Tedragon(t),
	'levyc':	lambda t: LevyC.LevyC(t),
	'sierpinsky':lambda t: Sierpinsky.Sierpinsky(t),
	'sierpinsky2':lambda t: Sierpinsky2.Sierpinsky2(t),
	'koch3D':	lambda t: KochCurve3D.KochCurve3D(t),
	'tree5':	lambda t: Tree5.Tree5(t),
	'tree6':	lambda t: Tree6.Tree6(t),
	'tree7':	lambda t: Tree7.Tree7(t),
	'default':	lambda t: HilbertCurve.HilbertCurve(t)
}

class Main:
	"""Entry point"""
	def __init__(self):
		self.turtle = Turtle()

		print "===== 3D L-system tracer - call 'help' for usage information ==="
		if not 'help' in sys.argv:
			self.gx = Graphx()

		[self.fractal, steps] = self.parse_input()
		self.fractal.setSteps(steps)

		self.quit = False
		self.follow_building = False


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
		self.gx.event(e)
		if self.fractal is not None:
			self.fractal.event(e)

	# handle command line argument
	def parse_input(self):
		lsys = None
		lsstep = 0
		for arg in sys.argv:
			if arg == 'help':
				print Conf.HELP
				exit()
			if arg == 'debug':
				print "Debug mode activated."
				Conf.DEBUG['lsystem'] = 1
			if arg in ARGUMENTS:
				lsys = ARGUMENTS[arg](self.turtle)
			try:
				lsstep = int(arg)
			except Exception, e:
				continue
		if lsys is None:
			print "Error: Unkonwn or unspecified fractal name."
			print Conf.HELP
			exit()
			#return (ARGUMENTS['default'](self.turtle), lsstep)
		return (lsys, lsstep)


	def main(self):
		t_init = time.time()

		self.fractal.generate()
		t_gen = time.time()
		print "Generation time: ", (t_gen - t_init), 'sec'

		self.fractal.runTurtleRun(stepbystep=('lsystem' in Conf.DEBUG and Conf.DEBUG['lsystem'] >= 1))
		print "Turtule running time: ", (time.time() - t_gen), 'sec'
		print "Total L-system creation time: ", (time.time() - t_init), 'sec'
		#print "OpenGL version:", glGetIntegerv(GL_MAJOR_VERSION)


		self.gx.setShader(self.fractal.getShader(), self.fractal.getUniforms())
		while not self.quit:
			for e in pygame.event.get():
				self.event(e)
			self.fractal.update()
			self.gx.clear(shader=self.fractal.getShader())
			self.turtle.draw()
			if self.follow_building:
				self.gx.update(self.turtle.pos.toTuple())
			else:
				self.gx.update()



Main().main()