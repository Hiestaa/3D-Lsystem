import pygame
from pygame.locals import *

import OpenGL.GL as gl
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


from Camera import Camera
from Conf import Conf

import numpy as np

class Graphx:
	"""Main class of the graphx engine"""
	def __init__(self):

		#glutInit(sys.argv)
		self.width, self.height = 1280, 800
		pygame.init()
		pygame.display.set_mode((self.width, self.height), OPENGL | DOUBLEBUF)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(65.0, self.width/float(self.height), 0.1, 1000.0)
		glMatrixMode(GL_MODELVIEW)
		glEnable(GL_DEPTH_TEST)
		self.camera = Camera((0.0, 100, 0), (0.0, 0, 0))

		#Base
		vertices = np.array([[100.0, -10.0, 100.0, Conf.GRAPHX.BASE_COLOR[0],Conf.GRAPHX.BASE_COLOR[1],Conf.GRAPHX.BASE_COLOR[2]], \
	    					[-100.0, -10.0, 100.0, Conf.GRAPHX.BASE_COLOR[0],Conf.GRAPHX.BASE_COLOR[1],Conf.GRAPHX.BASE_COLOR[2]], \
							[-100.0, -10.0, -100.0,Conf.GRAPHX.BASE_COLOR[0],Conf.GRAPHX.BASE_COLOR[1],Conf.GRAPHX.BASE_COLOR[2]], \
							[100.0, -10.0, -100.0, Conf.GRAPHX.BASE_COLOR[0],Conf.GRAPHX.BASE_COLOR[1],Conf.GRAPHX.BASE_COLOR[2]]], \
							dtype=np.float32)
		self.vertexPositions = vbo.VBO(vertices)
		#Create the index buffer object
		indices = np.array([[0,1,2], [0, 3, 2]], dtype=np.int32)
		self.indexPositions = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)

	  	#Now create the shaders
		self.VERTEX_SHADER = shaders.compileShader("""
		varying vec4 vertex_color;
		void main() {
			gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
			vertex_color = gl_Color;
		}
	    """, GL_VERTEX_SHADER)

		self.FRAGMENT_SHADER = shaders.compileShader("""
		varying vec4 vertex_color;
		void main() {
		    gl_FragColor = vertex_color;
		}
	    """, GL_FRAGMENT_SHADER)

		self.shader = shaders.compileProgram(self.VERTEX_SHADER, self.FRAGMENT_SHADER)


	def draw_base(self):


		self.indexPositions.bind()
		self.vertexPositions.bind()
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_COLOR_ARRAY)

		glVertexPointer(3, GL_FLOAT, 24, self.vertexPositions )
		glColorPointer(3, GL_FLOAT, 24, self.vertexPositions+12 )

		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

		self.indexPositions.unbind()
		self.vertexPositions.unbind()
		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_COLOR_ARRAY)


		# display axes
		glBegin(GL_LINES)
		glColor3f(0, 1, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(1, 0, 0);
		glColor3f(0, 0, 1)
		glVertex3f(0, 0, 0)
		glVertex3f(0, 1, 0);
		glColor3f(1, 0, 0)
		glVertex3f(0, 0, 0)
		glVertex3f(0, 0, 1);
		glEnd()


	def clear(self):
		#glClearColor(1,1,1,1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glUseProgram(self.shader)

	#display the base, update the camera and flip the display
	def update(self, lookat=(0, 0, 0)):
		self.camera.update()
		glMatrixMode( GL_MODELVIEW );
		glLoadIdentity( );
		self.camera.look(lookat);

		self.draw_base()

		pygame.display.flip()

	# handle events
	def event(self, e):
		self.camera.event(e)