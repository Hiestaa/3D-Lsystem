from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame

import numpy as np

def run():
    pygame.init()
    screen = pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

    #Create the VBO
    vertices = np.array([[0,1,0,1,0,0],[-1,-1,0,0,1,0],[1,-1,0,0,0,1]], dtype='f')
    vertexPositions = vbo.VBO(vertices)

    #Create the index buffer object
    indices = np.array([[0,1,2]], dtype=np.int32)
    indexPositions = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)

    #Now create the shaders
    VERTEX_SHADER = shaders.compileShader("""
	varying vec4 vertex_color;
	void main() {
		gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
		vertex_color = gl_Color;
	}
    """, GL_VERTEX_SHADER)

    FRAGMENT_SHADER = shaders.compileShader("""
	varying vec4 vertex_color;
	void main() {
	    gl_FragColor = vertex_color;
	}
    """, GL_FRAGMENT_SHADER)

    shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

    #The draw loop
    quit = False
    while not quit:
    	for e in pygame.event.get():
    		if e.type == pygame.QUIT or e.type == pygame.KEYDOWN:
				quit = True
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glUseProgram(shader)
		indexPositions.bind()
		vertexPositions.bind()

		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_COLOR_ARRAY)
		glVertexPointer(3, GL_FLOAT, 24, vertexPositions )
		glColorPointer(3, GL_FLOAT, 24, vertexPositions+12 )

		#glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
		glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None) #This line does work too!

		# Show the screen
		pygame.display.flip()


	indexPositions.unbind()
	vertexPositions.unbind()
    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_COLOR_ARRAY);
    glUseProgram( 0 )
run()