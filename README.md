3D-Lsystem
==========

A tool that can be used for Lindenmayer Systems fractals

Usage: ./3dlsystem [fractal_name] [fractal_step:int] ['debug']
	where fractal_name is can be:
		* 'tree1': A first try for drawing a 3D tree
		* 'tree2': A second 3D tree, much betted, with nice colors
		* 'tree2D': A tree, 2D version
		* 'tree3': A third 3D tree
		* 'tree3psy': The same tree as the previous one, buffed with LSD
		* 'tree4': Another 2D tree
		* 'tree5': A very fractalic-looking 3D tree
		* 'tree6': Another type of 3D tree with random factor
		* 'hilbert': The std hilbert curve
		* 'koch': The std koch curve
		* 'koch3D': a koch curve in 3D, like a diamond
		* 'dragon': the well known dragon curve (2D)
		* 'tedragon' the tedragon curve (2D)
		* 'levyc': The Levy Curve
		* 'sierpinsky': the sierpinsky carpet (some LSD added)
		* 'sierpinsky2': another version of the sierpinksy carpet (zoom to see the difference)
	and fractal_step is the precision of the fractal.
		For all the fractals, a default precision has been set so that it is interesting but not too hard to draw for your computer. You can increase this value but It's not advised to give much more for the safety of your computer...
	You can add the mention 'debug' to enable a step by step generation.

Here are the available controls in the display window:
	* **Left key**, **Right key**: control camera rotation speed
	* **Up key**, **Down key** or **mouse wheel*: zoom in/out
	* **Z**, **Q**, **S**, **D**, **A**, **E**: control scene rotation on x, y and z axis
	* **Space**: look at the last drawed point of the fractal
	* **Enter**: reinitialize the view
	* In debug mode :
		* **N**: Go to next step
		* **R**: Enable autorun. This will automatically run 5 steps by frame
		* **+**, **-**: Control autorun speed
