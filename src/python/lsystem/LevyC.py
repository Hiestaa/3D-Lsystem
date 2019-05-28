from lsystem.LSystem import LSystem
import math

class LevyC(LSystem):
	"""LevyC curve"""

	def defineParams(self):
		self.LSName = "LevyC curve"
		self.LSAngle = math.pi / 4
		self.LSSegment = 0.01
		self.LSSteps = 20
		self.LSStartingString = "--F"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'C':	self.turtle.nextColor,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ
		}
		self.LSParams = {
			'F':	self.LSSegment,
			'C':	0.000001,
			'+':	self.LSAngle,
			'-':	self.LSAngle
		}
	def createRules(self):
		self.LSRules = {
			'F':	"C+F--F+",
		}
