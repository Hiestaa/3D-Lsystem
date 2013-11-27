import math
from turtle.Turtle import *
from Conf import Conf
import pygame

class LSystem:
	"""Abstract class: allow generation of a L-System
	but does not own rules or variables
	You need to inherit from this class to implement your own l-system"""

	def __init__(self, turtle):
		self.turtle = turtle
		self.LSName = "Undefined" 	# nom de la fractale
		self.LSRules = {}		  	# regles de generation
		self.LSVars = {}		  	# variables = pointeurs sur actions de la turtle
		self.LSParams = {}		  	# parametres a appliquer aux actions de la turtle
		self.LSAngle = math.pi / 2	# angle (pour les rotations)
		self.LSSegment = 1.0		# taille d'un segment
		self.LSSteps = 5			# nombre de passe de generation (= precision de la fractale)
		self.LSSartingString = "F"	# axiome initial
		self.LSCode = ""			# code genere
		self.LSStochastic = False	# determine si le dessin doit etre aleatoire
		self.LSStochRange = 0.01	# determine le facteur aleatoire
		self.defineParams()
		self.createVars()
		self.createRules()
		self.currentMaxStep = 0
		self.currentStep = 0
		self.autorun = False
		self.stepbystep = False

	""" This method should set the following attributes of the fractal:
			- LSName: this is the name of the fractal
			- LSAngle: this is the default angle applied to rotations
			- LSSegment: this is the default segment length applied to forward or backward steps
			- LSSteps: this is the default number of steps done when recursively generating the code
			- LSStartingString: this is the starting code
	 """
	def defineParams(self):
		raise NotImplementedError("The method `defineParams' of the LSystem `" + self.LSName + "' has not been implemented yet")

	""" This method should fill in the LSVars dico that will associate actions of the turtle to some variables
	 and the LSParams dico what argument each function of the LSVars dico need  """
	def createVars(self):
		raise NotImplementedError("The method `createVars' of the LSystem `" + self.LSName + "' has not been implemented yet")

	""" This method should fill in the LSRules dico that will be used to recursively generate the fractal code"""
	def createRules(self):
		raise NotImplementedError("The method `createRules' of the LSystem `" + self.LSName + "' has not been implemented yet")

	def getCode(self):
		return self.LSCode

	def setSteps(self, n):
		self.LSSteps = n

	""" This method will recursively generate the code of the fractal"""
	def generate(self):
		print "============= Starting generation "
		print "============= LSName: ", self.LSName
		self.LSCode = self.LSSartingString
		self.generate_rec(self.LSSteps)
		if self.LSStochastic:
			self.turtle.setStochasticFactor(self.LSStochRange)
		self.LSCodeLen = len(self.LSCode)
		print "============= Generation DONE !"

	""" Run the turtle over the code of the fractal """
	def runTurtleRun(self, stepbystep=False):
		print "Starting turtle !"
		self.stepbystep = stepbystep

		# initialize step by step engine
		if self.stepbystep:
			self.currentStep = 0
			self.currentMaxStep = 0
			self.inc_max_step()

		# Begin the command sequence
		self.turtle.begin()
		if self.stepbystep:
			while self.currentStep < self.currentMaxStep:
				char = self.LSCode[self.currentStep]
				if char in self.LSVars:
					self.LSVars[char](self.LSParams[char])
				self.currentStep += 1
		else:
			count = 0
			for char in self.LSCode:
				count += 1
				if count % 50000 is 0:
					print "Turtle is running: ",
					percent = (float(count) / float(self.LSCodeLen) * 100)
					print "%.2f" % percent,
					print "% => [",
					print self.turtle.vertexBufferLength, "] vertex"
				if char in self.LSVars:
					# call the instruction corresponding to the current character
					self.LSVars[char](self.LSParams[char])
		self.turtle.end() # end the commend sequence

	""" Events handling """
	def event(self, e):
		if e.type == pygame.KEYDOWN and self.currentMaxStep < self.LSCodeLen:
			if e.unicode == 'n':
				if self.LSCode[self.currentMaxStep] in self.LSVars:
					print "Step: ", self.currentMaxStep, ": ",
					print self.LSVars[self.LSCode[self.currentMaxStep]].__name__ + "(" + str(self.LSParams[self.LSCode[self.currentMaxStep]]) + ")"
				self.inc_max_step()
			if e.unicode == 'r':
				self.autorun = not self.autorun
			if e.unicode == '+':
				Conf.LSYSTEM.AUTORUN_STEP *= 2
			if e.unicode == '-':
				Conf.LSYSTEM.AUTORUN_STEP /= 2

	""" This function allow to manage the step by step turtle running """
	def update(self):
		if self.stepbystep:
			self.turtle.begin()
			if self.autorun:
				self.inc_max_step(step=Conf.LSYSTEM.AUTORUN_STEP)
			while self.currentStep < self.currentMaxStep:
				char = self.LSCode[self.currentStep]
				if char in self.LSVars:
					self.LSVars[char](self.LSParams[char])
				self.currentStep += 1
			self.turtle.end()


	def generate_rec(self, iterations):
		if iterations == 0:
			return
		newcode = ''.join(map(self.get_rule, self.LSCode))


		self.LSCode = newcode

		print "============= Generation [" + str(self.LSSteps - iterations) + "], size=" + str(len(newcode)) + ": "
		if 'lsystem' in Conf.DEBUG and Conf.DEBUG['lsystem'] >= 2:
			print newcode

		self.generate_rec(iterations - 1)

	def get_rule(self, char):
		if char in self.LSRules:
			return self.LSRules[char]
		else:
			return char

	def inc_max_step(self, step=1):
		if self.currentMaxStep < self.LSCodeLen:
			self.currentMaxStep += step
			while self.currentMaxStep < self.LSCodeLen and self.LSCode[self.currentMaxStep] not in self.LSVars:
				self.currentMaxStep += 1
		if self.currentMaxStep >= self.LSCodeLen:
			self.currentMaxStep = self.LSCodeLen - 1