from lsystem.LSystem import LSystem
import math

class HilbertCurve(LSystem):
	"""Fractale courbe de hilbert"""

	def defineParams(self):
		self.LSName = "Hilbert Curve"
		self.LSAngle = math.pi / 2
		self.LSSegment = 0.1
		self.LSSteps = 6
		self.LSSartingString = "A"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotX,
			'-':	self.turtle.irotX
		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle
		}

	def createRules(self):
		self.LSRules = {
			'A':	"-BF+AFA+FB-",
			'B':	"+AF-BFB-FA+"
		}
