from lsystem.LSystem import LSystem
import math

class Sierpinsky(LSystem):
	"""Sierpinsky triangle"""

	def defineParams(self):
		self.LSName = "Sierpinsky triangle"
		self.LSAngle = 2 * math.pi / 3
		self.LSSegment = 0.01
		self.LSSteps = 12
		self.LSStartingString = "F-G-G"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'G':	self.turtle.forward,
			'C':	self.turtle.nextColor,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ
		}
		self.LSParams = {
			'F':	self.LSSegment,
			'G':	self.LSSegment,
			'C':	0.0001,
			'+':	self.LSAngle,
			'-':	self.LSAngle
		}
	def createRules(self):
		self.LSRules = {
			'F':	"CF-G+F+G-F",
			'G':	"GG"
		}
