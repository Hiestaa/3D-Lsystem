from Vector import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import pdb
import math

from Conf import Conf
import random
import numpy as np

class Turtle:
	"""This class is the turtle that will draw the fractals"""

	class State:
		"""This class represent a state of the turtle, for push and pop"""
		def __init__(self, pos, heading, color):
			self.pos = Vector().set(pos)
			self.heading = Vector().set(heading)
			self.color = Vector().set(color)

	def __init__(self):
		self.pos = Vector(Conf.TURTLE.INIT_POS)
		self.heading = Vector(Conf.TURTLE.INIT_HEADING)
		self.color = Vector(Conf.TURTLE.INIT_COLOR)

		self.stateStack = [] # allow to manage a stack of states
		self.stochasticFactor = 0 # used to randomize drawing

		# the vertex buffer is a liste of lists : [[x y z r g b breakline],...]
		self.vertexBuffer = []
		self.vertexBufferLength = 0
		self.vertexBufferChanged = False
		self.vertexPositions = None
		#indices = np.array([[0,1,2], [0, 3, 2]], dtype=np.int32)

	""" Set the stochastic factor of this instance of the turtle """
	def setStochasticFactor(self, factor):
		self.stochasticFactor = factor

	""" Return a random number in a range around the given number. The range is defined by the stochastoc factor """
	def randomize(self, value):
		if self.stochasticFactor:
			return ((random.random() * 2 * self.stochasticFactor) - self.stochasticFactor) * value + value
		return value

	""" Reinit the turtle to its initial state """
	def reinit(self):
		self.pos = Vector(Conf.TURTLE.INIT_POS)
		self.heading = Vector(Conf.TURTLE.INIT_HEADING)
		self.color = Vector(Conf.TURTLE.INIT_COLOR)
		self.vertexBuffer = []
		self.vertexBufferChanged = False
		self.vertexBufferLength = 0
		self.vertexPositions = vbo.VBO(np.array(self.vertexBuffer, dtype=np.float32))
		self.vertexPositions.bind()


	""" Draw a point at the current position of the turtle """
	def point(self, breakline = 0):
		self.vertexBuffer.append([float(self.pos.x), float(self.pos.y), float(self.pos.z),
							self.color.x, self.color.y, self.color.z, breakline])
		self.vertexBufferChanged = True
		self.vertexBufferLength += 1


	""" Begin a command list """
	def begin(self, reinit = False):
		# lorsque 'end()' est appele, si le vertexBuffer a change le vbo sera actualise
		self.vertexBufferChanged = False

		if reinit:
			self.reinit()
			glutSolidSphere(0.1, 10, 10)


	""" Push current state (pos, heading and color) on the state stack """
	def push(self, arg):
		if 'turtle' in Conf.DEBUG:
			print "Called: push"
		self.stateStack.append(Turtle.State(self.pos, self.heading, self.color))


	""" Rollback to the last pushed state of the state stack """
	def pop(self, arg):
		if 'turtle' in Conf.DEBUG:
			print "Called: pop"
		state = self.stateStack.pop()
		self.pos.set(state.pos)
		self.heading.set(state.heading)
		self.color.set(state.color)
		self.point(1)

	""" Move forward (draw a point) """
	def forward(self, step):
		if 'turtle' in Conf.DEBUG:
			print "Called: forward(", step, ");"
		#print "call: forward"
		self.pos += self.randomize(step) * self.heading
		self.point()

	""" Move backward (draw a point) """
	def backward(self, step):
		if 'turtle' in Conf.DEBUG:
			print "Called: backward(", step, ");"
		self.pos += ((self.randomize(step) * self.heading) * -1)
		self.point()

	""" Rotation around the x direction """
	def rotX(self, angle):
		if 'turtle' in Conf.DEBUG:
			print "Called: rotX(", angle, ");"
		angle = self.randomize(angle)
		self.heading.set((
			self.heading.x,
			self.heading.y * math.cos(angle) - self.heading.z * math.sin(angle),
			self.heading.y * math.sin(angle) + self.heading.z * math.cos(angle)))
	""" Reverse rotation around the x direction"""
	def irotX(self, angle):
		if 'turtle' in Conf.DEBUG:
			print "Called: rotX(", angle, ");"
		angle = self.randomize(angle)
		angle = -angle
		self.heading.set((
			self.heading.x,
			self.heading.y * math.cos(angle) - self.heading.z * math.sin(angle),
			self.heading.y * math.sin(angle) + self.heading.z * math.cos(angle)))

	""" Rotation around the y direction """
	def rotY(self, angle):
		if 'turtle' in Conf.DEBUG:
			print "Called: rotY(", angle, ");"
		angle = self.randomize(angle)
		self.heading.set((
			self.heading.x * math.cos(angle) + self.heading.z * math.sin(angle),
			self.heading.y,
			- self.heading.x * math.sin(angle) + self.heading.z * math.cos(angle)))
	""" Reverse rotation around the y direction"""
	def irotY(self, angle):
		if 'turtle' in Conf.DEBUG:
			print "Called: rotY(", angle, ");"
		angle = self.randomize(angle)
		angle = -angle
		self.heading.set((
			self.heading.x * math.cos(angle) + self.heading.z * math.sin(angle),
			self.heading.y,
			- self.heading.x * math.sin(angle) + self.heading.z * math.cos(angle)))

	""" Rotation around the z direction """
	def rotZ(self, angle):
		if 'turtle' in Conf.DEBUG:
			print "Called: rotZ(", angle, ");"
		angle = self.randomize(angle)
		self.heading.set((
			self.heading.x * math.cos(angle) - self.heading.y * math.sin(angle),
			self.heading.x * math.sin(angle) + self.heading.y * math.cos(angle),
			self.heading.z))
	""" Reverse rotation around the z direction"""
	def irotZ(self, angle):
		if 'turtle' in Conf.DEBUG:
			print "Called: rotZ(", angle, ");"
		angle = self.randomize(angle)
		angle = -angle
		self.heading.set((
			self.heading.x * math.cos(angle) - self.heading.y * math.sin(angle),
			self.heading.x * math.sin(angle) + self.heading.y * math.cos(angle),
			self.heading.z))

	def setColor(self, color):
		if 'turtle' in Conf.DEBUG:
			print "Called: setColor(", color, ");"
		color = self.randomize(color)
		self.color.set(color)

	""" Close a commend sequence """
	def end(self):
		glBegin(GL_LINES)
		glColor3f(0, 0, 1)
		glVertex3f(self.pos.x, self.pos.y, self.pos.z)
		glVertex3f(float(self.pos.x + self.heading.x), float(self.pos.y + self.heading.y), float(self.pos.z + self.heading.z));
		glEnd()

	""" Draw the turtle path """
	def draw(self):
		if self.vertexBufferChanged or self.vertexPositions is None:
			print "Vertex buffer changed !"
			#print "Creating numpy array..."
			vertices = np.array(self.vertexBuffer, \
		 					dtype=np.float32)
			print vertices
			#print "Creating VBO..."
			self.vertexPositions = vbo.VBO(vertices)
			print "VBO: ", self.vertexPositions.data
			#print "Total number of vertex #: ", self.vertexBufferLength
			self.vertexBufferChanged = False



		#self.indexPositions.bind()
		self.vertexPositions.bind()
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_COLOR_ARRAY)

		glVertexPointer(3, GL_FLOAT, 28, self.vertexPositions )
		glColorPointer(3, GL_FLOAT, 28, self.vertexPositions+12 )

		glDrawArrays(GL_LINE_STRIP, 0, self.vertexBufferLength);
		#glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

		#self.indexPositions.unbind()
		self.vertexPositions.unbind()
		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_COLOR_ARRAY)

