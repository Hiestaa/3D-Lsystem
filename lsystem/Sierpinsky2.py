from lsystem.LSystem import LSystem
import math
import time
from Conf import Conf

class Sierpinsky2(LSystem):
	"""Another way of drawing sierpinsky triangle"""

	def defineParams(self):
		self.LSName = "Sierpinsky, way 2"
		self.LSAngle = math.pi / 3
		self.LSSegment = 0.01
		self.LSSteps = 12
		self.LSStartingString = "A"

	def createVars(self):
		self.LSVars = {
			'A':	self.turtle.forward,
			'B':	self.turtle.forward,
			'C':	self.turtle.nextColor,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ,
		}
		self.LSParams = {
			'A':	self.LSSegment,
			'B':	self.LSSegment,
			'C':	0.0001,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
		}
	def createRules(self):
		self.LSRules = {
			'A':	"CB-A-B",
			'B':	"CA+B+A"
		}

	def createShaders(self):
		self.LSVertexShader = """

		uniform float time;
		varying vec4 vertex_color;

		void main() {
			vec3 col = rgb2hsv(gl_Color.xyz);
			gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
			col.x += 0.0001 * float(gl_VertexID) + (time * 0.1);
			if (col.x > 1.0) {
				col.x = fract(col.x);
			}
			vertex_color = vec4(hsv2rgb(col), 1);
		}
	    """
		self.LSPixelShader = """
		varying vec4 vertex_color;
		void main() {
		    gl_FragColor = vertex_color;
		}
		"""
		self.LSUniforms = {'time': lambda: time.time() - Conf.LAUNCH_TIME}
