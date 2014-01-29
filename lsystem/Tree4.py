from lsystem.LSystem import LSystem
import math

class Tree4(LSystem):
	"""Fractale en forme d'arbre, v4, avec facteur random"""

	def defineParams(self):
		self.LSName = "Tree 4"
		self.LSAngle = math.pi / 8
		self.LSSegment = 0.01
		self.LSSteps = 5
		self.LSStartingString = "X"
		self.LSStochastic = False

		self.LSStochRange = 1

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ,
			'^':	self.turtle.rotY,
			'&':	self.turtle.irotY,
			'<':	self.turtle.rotX,
			'>':	self.turtle.irotX,
			'|':	self.turtle.rotX,
			'[':	self.turtle.push,
			']':	self.turtle.pop,
			'I':	self.turtle.setColor,
			'Y':	self.turtle.setColor

		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'&':	self.LSAngle,
			'^':	self.LSAngle,
			'<':	self.LSAngle,
			'>':	self.LSAngle,
			'|':	self.LSAngle * 2,
			'[':	None,
			']':	None,
			'I':	(0.5,0.25,0),
			'Y':	(0, 0.5, 0)
		}

	def createRules(self):
		self.LSRules = {
			'X':	"F-[[X]+X]+F[+FX]-X",
			'F':	"FF"
		}
