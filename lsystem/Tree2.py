from lsystem.LSystem import LSystem
import math
import OpenGL.GL as gl

class Tree2(LSystem):
	"""Fractale en forme d'arbre, v2"""
	def __init__(self, turtle):
		super(Tree2, self).__init__(turtle)

	def defineParams(self):
		self.LSName = "Tree 2"
		self.LSAngle = math.pi / 16
		self.LSSegment = 1
		self.LSSteps = 4
		self.LSStartingString = "F"
		self.LSStochastic = True

		self.LSStochRange = 1
		self.LSDrawType = gl.GL_LINE_STRIP

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
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
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'&':	self.LSAngle,
			'^':	self.LSAngle,
			'<':	self.LSAngle / 2,
			'>':	self.LSAngle / 2,
			'|':	self.LSAngle * 2,
			'[':	None,
			']':	None,
			'I':	(0.5,0.25,0),
			'Y':	(0, 0.5, 0)
		}

	def createRules(self):
		self.LSRules = {
			'F':	"IFF-[Y-F+F+F]+[Y+F-F-F]<++[Y<++F>--F>--F]>--[Y>--F<++F<++F]"
		}
