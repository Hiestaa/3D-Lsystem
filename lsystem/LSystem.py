import math
from turtle.Turtle import *
from Conf import Conf
import pygame
from OpenGL.GL import shaders

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.GL.ARB.geometry_shader4 import *
from OpenGL.GL.EXT.geometry_shader4 import *

class LSystem(object):
	"""Abstract class: allow generation of a L-System
	but does not own rules or variables
	You need to inherit from this class to implement your own l-system"""

	def __init__(self, turtle):
		self.turtle = turtle
		self.LSName = "Undefined" 	# nom de la fractale
		self.LSRules = {}		  	# regles de generation
		self.LSVars = {}		  	# variables = pointeurs sur actions de la turtle
		self.LSParams = {}		  	# parametres a appliquer aux actions de la turtle
		self.LSAngle = math.pi / 2	# angle (pour les rotations)
		self.LSSegment = 1.0		# taille d'un segment
		self.LSSteps = 5			# nombre de passe de generation (= precision de la fractale)
		self.LSStartingString = "F"	# axiome initial
		self.LSCode = ""			# code genere
		self.LSStochastic = False	# determine si le dessin doit etre aleatoire
		self.LSStochRange = 0.01	# determine le facteur aleatoire
		self.LSVertexShader = ""	# vertex shader a appliquer a la fractale
		self.LSPixelShader = ""		# pixel shader a appliquer a la fractale
		self.LSUniforms = {}		# association nom-fonction des donnees uniform a associer au shader de cette fractale
		self.LSDrawType = GL_LINE_STRIP	# la facon dont les vertices du shader seront dessinees
		self.shaderProgram = None
		self.defineParams()
		self.createVars()
		self.createRules()
		self.currentMaxStep = 0
		self.currentStep = 0
		self.autorun = False
		self.stepbystep = False
		self.createShaders()
		self.compileShaders()

	""" This method should set the following attributes of the fractal:
			- LSName: this is the name of the fractal
			- LSAngle: this is the default angle applied to rotations
			- LSSegment: this is the default segment length applied to forward or backward steps
			- LSSteps: this is the default number of steps done when recursively generating the code
			- LSStartingString: this is the starting code
			- LSDrawType: the way the fractal is drawed (GL_LINES, GL_LINE_STRIP, GL_TRIANGLES, GL_TRIANGLE_STRIP, ...)
	 """
	def defineParams(self):
		raise NotImplementedError("The method `defineParams' of the LSystem `" + self.LSName + "' has not been implemented yet")

	""" This method should fill in the LSVars dico that will associate actions of the turtle to some variables
	 and the LSParams dico what argument each function of the LSVars dico need  """
	def createVars(self):
		raise NotImplementedError("The method `createVars' of the LSystem `" + self.LSName + "' has not been implemented yet")

	""" This method should fill in the LSRules dico that will be used to recursively generate the fractal code"""
	def createRules(self):
		raise NotImplementedError("The method `createRules' of the LSystem `" + self.LSName + "' has not been implemented yet")

	""" This method can change the default shaders applied to the fractal, and eventually set the LSUniforms associative array """
	def createShaders(self):
		self.LSVertexShader = """
// varying vec4 gl_Vertex;
// varying vec4 gl_Color;
uniform float time; // exemple of giving a uniform value
varying vec4 vertex_color;
void main() {
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	vertex_color = gl_Color;
}
	    """
		self.LSPixelShader = """
varying vec4 vertex_color;
void main() {
	gl_FragColor = vertex_color;
}
	    """
		self.LSUniforms = {
	    	'time': lambda: time.time() # a lambda function is used so that each time the shader is rendered, the value change
    	}

	#compile shaders
	# important note : if this function is not called after an openGL context has been defined,
	# it could crash the program with an error telling that a function is NULL
	def compileShaders(self):
		if not 'vec3 rgb2hsv(vec3 c)' in self.LSVertexShader:
			self.LSVertexShader = """
vec3 rgb2hsv(vec3 c)
{
	vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
	vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
	vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

	float d = q.x - min(q.w, q.y);
	float e = 1.0e-10;
	return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c)
{
	vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
	vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
	return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}
""" + self.LSVertexShader
		# if not '#version' in self.LSVertexShader:
		# 	self.LSVertexShader = '#version 320\n' + self.LSVertexShader
		# if not '#version' in self.LSPixelShader:
		# 	self.LSPixelShader = '#version 320\n' + self.LSPixelShader
		# VERTEX_SHADER = shaders.compileShader(self.LSVertexShader, GL_VERTEX_SHADER)

		# FRAGMENT_SHADER = shaders.compileShader(self.LSPixelShader, GL_FRAGMENT_SHADER)

		# self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

		vs = glCreateShader(GL_VERTEX_SHADER)
		fs = glCreateShader(GL_FRAGMENT_SHADER)
		#gs = glCreateShader(GL_GEOMETRY_SHADER_EXT)

		glShaderSource(vs, self.LSVertexShader)
		glShaderSource(fs, self.LSPixelShader)
		# glShaderSource(gs, source['geometry'])

		glCompileShader(vs)
		log = glGetShaderInfoLog(vs)
		if log:
			print "Vertex Shader: "
			print self.LSVertexShader
			print '>>>> Compilation Logs <<<< '
			print log

		# glCompileShader(gs)
		# log = glGetShaderInfoLog(gs)
		# if log: print 'Geometry Shader: ', log

		glCompileShader(fs)
		log = glGetShaderInfoLog(fs)
		if log:
			print "Pixel Shader: "
			print self.LSPixelShader
			print '>>>> Compilation Logs <<<< '
			print log

		self.shader = glCreateProgram()

		glAttachShader(self.shader, vs)
		glAttachShader(self.shader, fs)
		# glAttachShader(self.shader, gs)

		glLinkProgram(self.shader)

	def getShader(self):
		return self.shader

	def getUniforms(self):
		return self.LSUniforms

	def getCode(self):
		return self.LSCode

	def setSteps(self, n):
		if n < 1:
			self.LSSteps += n
		if self.LSSteps < 1:
			self.LSSteps = 1
		if n >= 1:
			self.LSSteps = n

	""" This method will recursively generate the code of the fractal"""
	def generate(self):
		print "============= Fractal Name: ", self.LSName
		print "============= Fractal Precision: ", self.LSSteps
		if self.LSStochastic:
			print "============= Fractal Stochastic Factor: ", self.LSStochRange
		print "============= LSystem Inital Axiom: ", self.LSStartingString
		print "============= LSystem Rules: "
		for r in self.LSRules:
			print '\t', r, "=>", self.LSRules[r]
		print "============= Starting generation. "
		self.LSCode = self.LSStartingString
		self.generate_param_rec(self.LSSteps)
		if self.LSStochastic:
			self.turtle.setStochasticFactor(self.LSStochRange)
		self.LSCodeLen = len(self.LSCode)
		print "============= Generation DONE !"

	""" Run the turtle over the code of the fractal """
	def runTurtleRun(self, stepbystep=False):
		print "Starting turtle !"
		self.stepbystep = stepbystep

		self.turtle.setDrawType(self.LSDrawType)

		# initialize step by step engine
		if self.stepbystep:
			self.currentStep = 0
			self.currentMaxStep = 0
			self.inc_max_step()

		# Begin the command sequence
		self.turtle.begin()
		if self.stepbystep:
			while self.currentStep < self.currentMaxStep:
				tmp = [self.currentStep];
				self.execute(tmp)
				self.currentStep = tmp[0]
		else:
			count = [0]
			while count[0] < self.LSCodeLen:
				#count[0] += 1
				if count[0] % 50000 is 0:
					print "Turtle is running: ",
					percent = (float(count[0]) / float(self.LSCodeLen) * 100)
					print "%.2f" % percent,
					print "% => [",
					print self.turtle.vertexBufferLength, "] vertex"
				self.execute(count)
		self.turtle.end() # end the commend sequence

	# execute the current instruction, using the eventual parameters
	# pos will be incremented
	def execute(self, pos):
		dbg = pos[0]
		char = self.LSCode[pos[0]];
		if pos[0] + 1 < self.LSCodeLen and self.LSCode[pos[0] + 1] == '(':
			#print "Step: ", pos[0], ": ",
			arg = self.find_arg(pos) # extract arguments of the instruction
			if arg is None:
				print "Error: no argument found for inst `"+char+"' in: ", self.LSCode[dbg:dbg+10]
				return;
			# if we are executing a parametized rule:
			# replace each variable by its value in the params array
			for param in self.LSParams:
				if param in arg:
					arg = arg.replace(param, str(float(self.LSParams[param])))
			res = eval(arg) # evaluate expression

			#print self.LSVars[char].__name__ + "(" + str(res) + ")"

			if char in self.LSVars:
				self.LSVars[char](res)	# call corresponding function, giving the parameter
		else:
			#print "Step: ", pos[0], ": ",
			#print self.LSVars[char].__name__ + "(" + str(self.LSParams[char]) + ")"
			if char in self.LSVars:
				self.LSVars[char](self.LSParams[char])	# call corresponding function, giving the parameter
			pos[0] += 1 	# increase look ahead



	""" Events handling """
	def event(self, e):
		if e.type == pygame.KEYDOWN and self.currentMaxStep < self.LSCodeLen:
			if e.unicode == 'n':
				self.inc_max_step()
			if e.unicode == 'r':
				self.autorun = not self.autorun
			if e.unicode == '+':
				Conf.LSYSTEM.AUTORUN_STEP *= 10
			if e.unicode == '-':
				Conf.LSYSTEM.AUTORUN_STEP /= 10

	""" This function allow to manage the step by step turtle running """
	def update(self):
		if self.stepbystep:
			self.turtle.begin()
			if self.autorun:
				self.inc_max_step(step=Conf.LSYSTEM.AUTORUN_STEP)
			while self.currentStep < self.currentMaxStep:
				#pdb.set_trace()
				tmp = [self.currentStep];
				self.execute(tmp)
				self.currentStep = tmp[0]
			self.turtle.end()


	def generate_rec(self, iterations):
		if iterations == 0:
			return
		newcode = ''.join(map(self.get_rule, self.LSCode))


		self.LSCode = newcode

		print "============= Generation [" + str(self.LSSteps - iterations) + "], size=" + str(len(newcode)) + ": "
		if 'lsystem' in Conf.DEBUG and Conf.DEBUG['lsystem'] >= 2:
			print newcode

		self.generate_rec(iterations - 1)

	# Allow to recursively generate the code, keeping attention to the code parameters
	def generate_param_rec(self, itern):
		#pdb.set_trace()
		self.LSCodeLen = len(self.LSCode)
		if itern == 0:
			return

		rplc_list = []
		la = [0] # look ahead

		# traverse the code string and create the replacement string lists
		while la[0] < self.LSCodeLen:
			rplc_list.append(self.apply_rule(la))

		newcode = ''.join(rplc_list)

		self.LSCode = newcode

		print "============= Generation [" + str(self.LSSteps - itern + 1) + "], size=" + str(len(newcode)) + ": "
		if 'lsystem' in Conf.DEBUG and Conf.DEBUG['lsystem'] >= 2:
			print newcode

		self.generate_param_rec(itern - 1)

	# build the replacement string of the current token
	# move the look ahead
	def apply_rule(self, la):
		char = self.LSCode[la[0]] # get current character
		r = self.rules_contain(char) # get the corresponding rule
		#pdb.set_trace()
		if r: # if rule is set, we need to find the parameter given to the rule
			arg = self.find_arg(la)
			# None arg means that the rule is not parametized
			if not arg:
				return self.LSRules[r] # just return the rule
			param = self.find_param(r) # find the param name of the rule
			parametized_rule = self.LSRules[r].replace(param, arg) # replace the param name by its value
			#print char, '(', arg, ')', '=', parametized_rule
			#if parametized_rule == 'F(x/2)+F(x/2/2)':
			#	pdb.set_trace()
			return parametized_rule

		else: # if no rule is defined, just return the character
			la[0] += 1 	# increase look ahead
			return char

	def find_param(self, r):
		ob = 0
		cb = 0
		for k in range(len(r)):
			if r[k] == '(':
				ob = k
			if r[k] == ')':
				cb = k
		if cb is 0 or cb is ob:
			return None
		return r[ob+1:cb]


	# find the argument given to this function
	# la must point on the name of the function
	def find_arg(self, la):
		# go to next caracter
		la[0] += 1
		if la[0] >= self.LSCodeLen:
			return None
		# if current character is not '('
		# we are not on a parametized rule
		if self.LSCode[la[0]] != '(':
			return None
		k = la[0]
		while self.LSCode[k] != ')':
			k += 1 # find the closing bracket
		res = self.LSCode[la[0]+1:k] # substring
		la[0] = k + 1;
		return res


	def rules_contain(self, char):
		for r in self.LSRules:
			if r[0] == char: # the rule is 1char named
				return r
		return False

	def get_rule(self, char):
		if char in self.LSRules:
			return self.LSRules[char]
		else:
			return char

	def inc_max_step(self, step=1):
		if self.currentMaxStep < self.LSCodeLen:
			self.currentMaxStep += step
			while self.currentMaxStep < self.LSCodeLen and self.LSCode[self.currentMaxStep] not in self.LSVars:
				self.currentMaxStep += 1
		if self.currentMaxStep >= self.LSCodeLen:
			self.currentMaxStep = self.LSCodeLen - 1
