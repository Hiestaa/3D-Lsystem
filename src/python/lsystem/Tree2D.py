from lsystem.LSystem import LSystem
import math

class Tree2D(LSystem):
	"""Fractale en forme d'arbre en 2D"""

	def defineParams(self):
		self.LSName = "Tree 3"
		self.LSAngle = math.pi / 4
		self.LSSegment = 0.01
		self.LSSteps = 8
		self.LSStartingString = "F"
		self.LSStochastic = False
		self.LSStochRange = 0.1

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
			']':	self.turtle.pop

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
			']':	None
		}

	def createRules(self):
		self.LSRules = {
			'F':	"FF[-F][+F]"
		}
