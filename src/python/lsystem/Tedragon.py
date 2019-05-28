from lsystem.LSystem import LSystem
import math

class Tedragon(LSystem):
	"""Tedragon curve"""

	def defineParams(self):
		self.LSName = "Tedragon curve"
		self.LSAngle = 2 * math.pi / 3
		self.LSSegment = 0.01
		self.LSSteps = 13
		self.LSStartingString = "F"

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
			'F':	"CF+F-F",
		}
