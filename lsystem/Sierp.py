from lsystem.LSystem import LSystem
import math

class Sierp(LSystem):
	"""Fractale courbe de koch"""

	def defineParams(self):
		self.LSName = "Sierp"
		self.LSAngle = math.pi / 3
		self.LSSegment = 1
		self.LSSteps = 2
		self.LSSartingString = "F"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ,
			'>':	self.turtle.rotX,
			'<':	self.turtle.irotX,
			'&':	self.turtle.rotY
		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'>':	self.LSAngle,
			'<':	self.LSAngle,
			'&':	math.pi / 4
		}
	def createRules(self):
		self.LSRules = {
			'F':	"F+F-X-F+F",
			'X':	""#"[[<F>F]&&[<F>F]]"
		}
			