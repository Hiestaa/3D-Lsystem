import time

LSCode = 'F'
LSRules = {'F'	:	'F+F-F-F+F'}
LSSteps = 11



def generate_rec1(iterations):
	global LSCode
	if iterations == 0:
		return
	newcode = ''.join([get_rule(char) for char in LSCode])


	LSCode = newcode

	print "============= Generation [" + str(LSSteps - iterations) + "], size=" + str(len(newcode)) + ": "
	generate_rec1(iterations - 1)

def generate_rec2(iterations):
	global LSCode
	if iterations == 0:
		return
	newcode = ''.join(map(get_rule, LSCode))


	LSCode = newcode

	print "============= Generation [" + str(LSSteps - iterations) + "], size=" + str(len(newcode)) + ": "
	generate_rec1(iterations - 1)

def get_rule(char):
	if char in LSRules:
		return LSRules[char]
	else:
		return char



print ">>>> Starting benchmark... "
print ">>>> Testing: generate_rec1"
beg = time.time()
generate_rec1(LSSteps)
print ">>>> DONE !"
print "Time of execution: ", (time.time() - beg), 's'
LSCode = 'F'
print ">>>> Testing: generate_rec1"
beg = time.time()
generate_rec2(LSSteps)
print ">>>> DONE !"
print "Time of execution: ", (time.time() - beg), 's'
