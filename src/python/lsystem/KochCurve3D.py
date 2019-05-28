from lsystem.LSystem import LSystem
import math

class KochCurve3D(LSystem):
	"""Fractale courbe de koch en 3D"""

	def defineParams(self):
		self.LSName = "Koch curve 3D"
		self.LSAngle = math.pi / 2
		self.LSSegment = 0.01
		self.LSSteps = 8
		self.LSStartingString = "A"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'G':	self.turtle.forward,
			'H':	self.turtle.forward,
			'I':	self.turtle.forward,
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
			'G':	self.LSSegment,
			'H':	self.LSSegment,
			'I':	self.LSSegment,
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
			'A':	"[[[[F+F-F-F+F]G<G>G>G<G]H-H+H+H-H]I>I<I<I>I]",
			'F':	"F+F-F-F+F",
			'G':	"G<G>G>G<G",
			'H':	"H-H+H+H-H",
			'I':	"I>I<I<I>I",
		}
