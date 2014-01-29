from lsystem.LSystem import LSystem
import math

class HilbertCurve3D(LSystem):
	"""Fractale courbe de hilbert en 3D"""

	def defineParams(self):
		self.LSName = "Hilbert Curve"
		self.LSAngle = math.pi / 2
		self.LSSegment = 1.0
		self.LSSteps = 2
		self.LSStartingString = "X"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ,
			'^':	self.turtle.rotX,
			'&':	self.turtle.irotX,
			'<':	self.turtle.rotY,
			'>':	self.turtle.irotY

		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'&':	self.LSAngle,
			'^':	self.LSAngle,
			'<':	self.LSAngle,
			'>':	self.LSAngle
		}

	def createRules(self):
		self.LSRules = {
			'X':	"^<XF^<XFX-F^>>XFX&F+>>XFX-F>X->"
		}
