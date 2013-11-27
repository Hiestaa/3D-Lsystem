class Conf:
	"""Configuration file"""

	class TURTLE:
		""" Configuration of the turtle """
		INIT_POS = (0, 0, 0) # initial position
		INIT_HEADING = (0, 1, 0) # initial heading
		INIT_COLOR = (1, 0, 0) # initial color
#		INIT_UP = (0, 1, 0)
		APPEND_STEP = 10000

	class GRAPHX:
		BASE_COLOR = (0.2, 0.2, 0.2)
		CAMERA_UPDATE_PERIOD = 1
		CAMERA_ROTATION_VELOC = 0.1

	class LSYSTEM:
		AUTORUN_STEP = 5

	DEBUG = {
		#'lsystem': 1,
		#'turtle'
	}

	HELP = \
"""Usage: ./3dlsystem [fractal_name] [fractal_step:int]
	where fractal_name is can be:
		'tree1': A first try for drawing a 3D tree
		'tree2': A second 3D tree, much betted, with nice colors
		'tree2D': A tree, 2D version
		'tree3': A third 3D tree
		'hilbert': The std hilbert curve
		'koch': The std koch curve
		'koch3D': a koch curve in 3D, like a diamond
	and fractal_step is the precision of the fractal.
		It's not advised to give much more than 6 or 7 for the safety of your computer...
"""
