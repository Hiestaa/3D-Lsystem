from lsystem.LSystem import LSystem
import math

class KochCurve(LSystem):
	"""Fractale courbe de koch"""

	def defineParams(self):
		self.LSName = "Koch curve"
		self.LSAngle = math.pi / 2
		self.LSSegment = 0.01
		self.LSSteps = 9
		self.LSStartingString = "F"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ
		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle
		}
	def createRules(self):
		self.LSRules = {
			'F':	"F+F-F-F+F"
		}
