from lsystem.LSystem import LSystem
import math

class Tree2(LSystem):
	"""Fractale en forme d'arbre, v1"""

	def defineParams(self):
		self.LSName = "Tree 2"
		self.LSAngle = math.pi / 8
		self.LSSegment = 1
		self.LSSteps = 4
		self.LSSartingString = "F"
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
			'<':	self.LSAngle / 2,
			'>':	self.LSAngle / 2,
			'|':	self.LSAngle * 2,
			'[':	None,
			']':	None,
			'I':	(0.5,0.25,0),
			'Y':	(0, 0.5, 0)
		}

	def createRules(self):
		self.LSRules = {
			'F':	"IFF-[Y-F+F+F]+[Y+F-F-F]<++[Y<++F>--F>--F]>--[Y>--F<++F<++F]"
		}
