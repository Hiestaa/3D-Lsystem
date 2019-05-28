import time

class Conf:
	"""Configuration file"""
	LAUNCH_TIME = time.time()

	class TURTLE:
		""" Configuration of the turtle """
		INIT_POS = (0, 0, 0) # initial position
		INIT_HEADING = (0, 1, 0) # initial heading
		INIT_COLOR = (0.5, 0.25, 0.0) # initial color
#        INIT_COLOR = (0.5, 0.25, 0) # initial color
		APPEND_STEP = 2

	class GRAPHX:
		BASE_COLOR = (0.2, 0.2, 0.2)
		CAMERA_UPDATE_PERIOD = 1
		CAMERA_ROTATION_VELOC = 0.1

	class LSYSTEM:
		AUTORUN_STEP = 5

	DEBUG = {
		'lsystem': 0,
		#'turtle': 1
	}

	HELP = \
"""Usage: ./3dlsystem.py [fractal_name] [fractal_step:int] ['debug']
  where fractal_name is can be:
    'tree1': A first try for drawing a 3D tree
    'tree2': A second 3D tree, much betted, with nice colors
    'tree2D': A tree, 2D version
    'tree3': A third 3D tree
    'tree3psy': The same tree as the previous one, buffed with LSD
    'tree4': Another 2D tree
    'tree5': A very fractalic-looking 3D tree
    'tree6': Another type of 3D tree with random factor
    'hilbert': The std hilbert curve
    'koch': The std koch curve
    'koch3D': a koch curve in 3D, like a diamond
    'dragon': the well known dragon curve (2D)
    'tedragon' the tedragon curve (2D)
    'levyc': The Levy Curve
    'sierpinsky': the sierpinsky carpet (some LSD added)
    'sierpinsky2': another version of the sierpinksy carpet
            (zoom to see the difference)
  and fractal_step is the precision of the fractal.
    It's not advised to give much more than 6 or 7 for the safety of your
    computer...
    For each fractal, a default step number has been set wich an average
    interessant value. You can specify a negative number to decrease the
    default step number.
  You can add the mention 'debug' to enable a step by step generation.

  Here are the available controls in the display window:
    - Left/Right key: control camera rotation speed
    - Up/Down key or mouse wheel: zoom in/out
    - z/q/s/d/a/e : rotate the fractal
    - space : look at the last drawd point of the fractal
    - enter : reinitialize the view
    - In debug mode:
      - n: go to next step
      - r: enable autorun: this will automatically run 5 steps by frame
      - +/-: control autorun speed. Do not increase autorun speed to much
      to keep an acceptable framerate.
"""
	FOREST_HELP = \
"""Usage: ./forest.py [size=S] [fractal=F] [random=R] [debug[=True|False]]
  Where the parameters can be precised in any order, and means:
    - S: int >= 1 is the size of the forest.
        The fractal number will be set to S squared.
        Default value is 10
    - F: int is a modificator of the precision of
        the fractals that will be generated.
        Any positive or negative number can be specified,
        but values higher than 2 or 3 are not advised.
        Default value is -2.
    - R: float > 0 is the random factor for the placement of the
        fractal trees.
        By default, it is computed according to the size of
        the grid
    - debug allow to enter debug mode

  Here are the available controls in the display window:
    - Left/Right key: control camera rotation speed
    - Up/Down key or mouse wheel: zoom in/out
    - z/q/s/d/a/e : rotate the fractal
    - space : look at the last drawd point of the fractal
    - enter : reinitialize the view
    - In debug mode:
      - n: go to next step
      - r: enable autorun: this will automatically run 5 steps by frame
      - +/-: control autorun speed. Do not increase autorun speed to much
      to keep an acceptable framerate.
"""
