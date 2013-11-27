3D-Lsystem
==========

A tool that can be used for Lindenmayer Systems fractals

Usage: ./3dlsystem [fractal_name] [fractal_step:int] ['debug']
	where fractal_name is can be:
		* 'tree1': A first try for drawing a 3D tree
		* 'tree2': A second 3D tree, much betted, with nice colors
		* 'tree2D': A tree, 2D version
		* 'tree3': A third 3D tree
		* 'hilbert': The std hilbert curve
		* 'koch': The std koch curve
		* 'koch3D': a koch curve in 3D, like a diamond
	and fractal_step is the precision of the fractal.
		It's not advised to give much more than 6 or 7 for the safety of your computer...
	You can add the mention 'debug' to enable a step by step generation.

Controls:
	* **Left key**, **Right key**: control camera rotation speed
	* **Z**, **Q**, **S**, **D**, **A**, **E**: control scene rotation on x, y and z axis
	* In debug mode :
		* **N**: Go to next step
		* **R**: Enable autorun. This will automatically run 5 steps by frame
		* **+**, **-**: Control autorun speed
