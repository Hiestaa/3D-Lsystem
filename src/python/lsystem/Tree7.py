from lsystem.LSystem import LSystem
import math

class Tree7(LSystem):
	"""Fractale en forme d'arbre v7"""

	def defineParams(self):
		self.LSName = "Tree7"
		self.LSAngle = math.pi / 4
		self.LSSegment = 100
		self.LSSteps = 9
		self.LSStartingString = "T(x)"
		self.LSStochastic = False

		self.LSStochRange = 0.2

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'T':	self.turtle.forward,
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
			'x':	self.LSSegment,
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
		    "T(x)":	"IT(x*0.3)F(x*0.3)",
		    "F(x)":	"IF(x)[+YF(x*0.5)][-YF(x*0.5)][<YF(x*0.5)][>YF(x*0.5)]"
		}
