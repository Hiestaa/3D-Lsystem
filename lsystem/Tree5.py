from lsystem.LSystem import LSystem
import math

class Tree5(LSystem):
	"""Fractale en forme d'arbre v5"""
	def __init__(self, turtle, modif_seg = 0, modif_angle = 0, modif_factor = 0.6):
		self.modif_seg = modif_seg
		self.modif_angle = modif_angle
		self.modif_factor = modif_factor
		super(Tree5, self).__init__(turtle)

	def defineParams(self):
		self.LSName = "Tree5"
		self.LSAngle = math.pi / 4 + self.modif_angle
		self.LSSegment = 5 + self.modif_seg
		self.LSSteps = 8
		self.LSStartingString = "T(x)"
		self.LSStochastic = False

		self.LSStochRange = 0.2

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'B':	self.turtle.forward,
			'T':	self.turtle.forward,
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
			'B':	-self.LSSegment,
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
		    "T(x)":	"IT(x)F(x)",
		    "F(x)":	"IF(x)[+YF(x*"+str(self.modif_factor)+")][-YF(x*"+str(self.modif_factor)+")][<YF(x*"+str(self.modif_factor)+")][>YF(x*"+str(self.modif_factor)+")]"
		}
