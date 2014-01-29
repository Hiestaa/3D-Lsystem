from lsystem.LSystem import LSystem
import math

class Tree6(LSystem):
	"""Fractale en forme d'arbre v6"""
	def __init__(self, turtle, modif_seg = 0, modif_angle = 0):
		self.modif_seg = modif_seg
		self.modif_angle = modif_angle
		super(Tree6, self).__init__(turtle)

	def defineParams(self):
		self.LSName = "Tree6"
		self.LSAngle = math.pi / 4 + self.modif_angle
		self.LSSegment = 10 + self.modif_seg
		self.LSSteps = 8
		self.LSStartingString = "T(x)"
		self.LSStochastic = True

		self.LSStochRange = 0.5

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'T':	self.turtle.forward,
			'G':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ,
			'^':	self.turtle.rotY,
			'&':	self.turtle.irotY,
			'<':	self.turtle.rotX,
			'>':	self.turtle.irotX,
			'|':	self.turtle.rotX,
			'[':	self.turtle.push,
			']':	self.turtle.pop,
			'I':	self.turtle.setColor,
			'Y':	self.turtle.setColor

		}
		self.LSParams = {
			'x':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'&':	self.LSAngle,
			'^':	self.LSAngle,
			'<':	self.LSAngle,
			'>':	self.LSAngle,
			'|':	self.LSAngle * 2,
			'[':	None,
			']':	None,
			'I':	(0.5,0.25,0),
			'Y':	(0, 0.5, 0)
		}

	def createRules(self):
		self.LSRules = {
		    "T(x)":	"IG(x)F(x)",
		    "G(x)": "G(x)",
		    "F(x)":	"IF(x)[+YF(x*0.6)][-YF(x*0.6)][<YF(x*0.6)][>YF(x*0.6)]"
		}
