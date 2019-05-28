from lsystem.LSystem import LSystem
import math

class FirstTree(LSystem):
	"""Fractale en forme d'arbre, v1"""
	def __init__(self, turtle):
		super(FirstTree, self).__init__(turtle)

	def defineParams(self):
		self.LSName = "First tree"
		self.LSAngle = math.pi / 8
		self.LSSegment = 1
		self.LSSteps = 6
		self.LSStartingString = "CF"

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
			'C':	self.turtle.setColor

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
			'C':	(0, 0.5, 0)
		}

	def createRules(self):
		self.LSRules = {
			'F':	"F[-&<F][<++&F]||F[--&>F][+&F]"
		}
