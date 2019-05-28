# 3D-Lsystem

A tool that can be used for Lindenmayer Systems fractals. The tool is made of two parts, as shown below.
To launch the program, the following programs and libraries are required:
* python v2.7.6,
* OpenGL and the pyOpenGL binding for the visualization
* 	pygame for the context window.

You can see an overview of what the program can display in the results folder.

The file "Génération de nature fractale.pdf" is the report of the project but I'm sorry, for my exam it had to be written in french. I did not have the time to translate it.

## Simple fractal generator

Usage: `./3dlsystem [fractal_name] [fractal_step:int] ['debug']`
where fractal_step is the precision of the fractal and fractal_name can be:
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

For all the fractals, a default precision has been set so that it is interesting but not too hard to draw for your computer.
You can increase this value but it's not advised to give much more for the safety of your computer...

You can add the mention 'debug' to enable a step by step generation.

Here are the available controls in the display window:
* **Left key**, **Right key**: control camera rotation speed
* **Up key**, **Down key** or **mouse wheel*: zoom in/out
* **Z**, **Q**, **S**, **D**, **A**, **E**: control scene rotation on x, y and z axis
* **Space**: look at the last drawed point of the fractal
* **Enter**: reinitialize the view

In debug mode :
* **N**: Go to next step
* **R**: Enable autorun. This will automatically run 5 steps by frame
* **+**, **-**: Control autorun speed

## Forest generator

The purpose of this script is to generate a fractal forest using many different fractal trees.

Usage: `./forest.py [size=S] [fractal=F] [random=R] [debug[=True|False]]`
where the parameters can be precised in any order, and means:
* S: int >= 1 is the size of the forest.
The fractal number will be set to S squared. Default value is 10
* F: int is a modificator of the precision of
the fractals that will be generated.
Any positive or negative number can be specified,
but values higher than 2 or 3 are not advised.
Default value is -2.
* R: float > 0 is the random factor for the placement of the
fractal trees.
By default, it is computed according to the size of
the grid
* debug allow to enter debug mode

Here are the available controls in the display window:
* **Left key**, **Right key**: control camera rotation speed
* **Up key**, **Down key** or **mouse wheel*: zoom in/out
* **Z**, **Q**, **S**, **D**, **A**, **E**: control scene rotation on x, y and z axis
* **Space**: look at the last drawed point of the fractal
* **Enter**: reinitialize the view

In debug mode:
* **N**: Go to next step
* **R**: Enable autorun. This will automatically run 5 steps by frame
* **+**, **-**: Control autorun speed Do not increase autorun speed to much
to keep an acceptable framerate.
