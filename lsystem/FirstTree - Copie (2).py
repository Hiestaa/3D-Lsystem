from lsystem.LSystem import LSystem
import math

class FirstTree(LSystem):
	"""Fractale en forme d'arbre, v1"""

	def defineParams(self):
		self.LSName = "First tree"
		self.LSAngle = math.pi / 8
		self.LSSegment = 1
		self.LSSteps = 4
		self.LSSartingString = "F"

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
			'F':	"F[-&<F][<++&F]||F[--&>F][+&F]"
		}
			