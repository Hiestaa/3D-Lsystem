import math
from turtle.Turtle import *
from Conf import Conf
import pygame

class LSystem:
	"""Classe abstraite : permet de faire la generation et l'affichage
	mais ne contient pas de regles ou de variables"""
	def __init__(self, turtle):
		self.turtle = turtle
		self.LSName = "Undefined" 	# nom de la fractale
		self.LSRules = {}		  	# regles de generation
		self.LSVars = {}		  	# variables = pointeurs sur actions de la turtle
		self.LSParams = {}		  	# parametres a appliquer aux actions de la turtle
		self.LSAngle = math.pi / 2	# angle (pour les rotations)
		self.LSSegment = 1.0		# taille d'un segment
		self.LSSteps = 5			# nombre de passe de generation (= precision de la fractale)
		self.LSStartingString = "F"	# axiome initial
		self.LSCode = ""			# code genere
		self.LSStochastic = False	# determine si le dessin doit etre aleatoire
		self.LSStochRange = 0.01	# determine le facteur aleatoire
		self.defineParams()
		self.createVars()
		self.createRules()
		self.currentMaxStep = 0
		self.currentStep = 0
		self.autorun = False

	def defineParams(self):
		raise NotImplementedError("The method `defineParams' of the LSystem `" + self.LSName + "' has not been implemented yet")

	def createVars(self):
		raise NotImplementedError("The method `createVars' of the LSystem `" + self.LSName + "' has not been implemented yet")

	def createRules(self):
		raise NotImplementedError("The method `createRules' of the LSystem `" + self.LSName + "' has not been implemented yet")

	def getCode(self):
		return self.LSCode

	def generate(self):
		print "============= Starting generation "
		print "============= LSName: ", self.LSName
		self.LSCode = self.LSStartingString
		self.generate_rec(self.LSSteps)
		if self.LSStochastic:
			self.turtle.setStochasticFactor(self.LSStochRange)
		self.LSCodeLen = len(self.LSCode)
		print "============= Generation DONE !"

	def event(self, e):
		if e.type == pygame.KEYDOWN and self.currentMaxStep < self.LSCodeLen:
			if e.unicode == 'n':
				if self.LSCode[self.currentMaxStep] in self.LSVars:
					print "Step: ", self.currentMaxStep, ": ",
					print self.LSVars[self.LSCode[self.currentMaxStep]].__name__ + "(" + str(self.LSParams[self.LSCode[self.currentMaxStep]]) + ")"
				self.inc_max_step()
			if e.unicode == 'r':
				self.autorun = not self.autorun

	def runTurtleRun(self, stepbystep=False):
		# gestion de l'autorun : si 'vrai', chaque appel lance automatiquement la tortue une etape plus loin
		if self.autorun:
			self.inc_max_step()

		# lancement de la tortue
		self.turtle.begin()
		if stepbystep:
			k = -1
			for char in self.LSCode:
				k += 1
				if char in self.LSVars and k < self.currentMaxStep:
					self.LSVars[char](self.LSParams[char])
		else:
			for char in self.LSCode:
				if char in self.LSVars:
					self.LSVars[char](self.LSParams[char])
		self.turtle.end()

	def generate_rec(self, iterations):
		if iterations == 0:
			return
		newcode = ''.join(map(self.get_rule, self.LSCode))


		self.LSCode = newcode

		print "============= Generation [" + str(self.LSSteps - iterations) + "], size=" + str(len(newcode)) + ": "
		if 'lsystem' in Conf.DEBUG and Conf.DEBUG['lsystem'] >= 1:
			print newcode

		self.generate_rec(iterations - 1)

	def get_rule(self, char):
		if char in self.LSRules:
			return self.LSRules[char]
		else:
			return char

	def inc_max_step(self):
		if self.currentMaxStep < self.LSCodeLen:
			self.currentMaxStep += 1
			while self.currentMaxStep < self.LSCodeLen and self.LSCode[self.currentMaxStep] not in self.LSVars:
				self.currentMaxStep += 1