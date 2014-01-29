from lsystem.LSystem import LSystem
from Conf import Conf
import math
import time

class Tree3psy(LSystem):
	"""Fractale en forme d'arbre, v3, psyche version"""

	def defineParams(self):
		self.LSName = "Tree 3"
		self.LSAngle = math.pi / 8
		self.LSSegment = 1
		self.LSSteps = 6
		self.LSStartingString = "F"
		self.LSStochastic = False

		self.LSStochRange = 0.1

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
			'N':	self.turtle.nextColor,

		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'&':	self.LSAngle,
			'^':	self.LSAngle,
			'<':	self.LSAngle,
			'>':	self.LSAngle,
			'|':	self.LSAngle * 2,
			'[':	None,
			']':	None,
			'N': 	0.01
		}

	def createRules(self):
		self.LSRules = {
			'F':	"NFF[-FF][+FF][<FF][>FF]"
		}

	def createShaders(self):
		self.LSVertexShader = """
		in vec4 gl_Vertex;
		in vec4 gl_Color;
		uniform float time;
		varying vec4 vertex_color;

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

		void main() {
			vec3 col = rgb2hsv(gl_Color.xyz);
			gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
			col.x +=  - (time * 0.1);
			while (col.x > 1) {
				col.x -= 1;
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

