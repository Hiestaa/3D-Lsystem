class Vector:
	"""represente un vecteur 3d"""
	def __init__(self, arg = (0, 0, 0)):
		self.x = float(arg[0])
		self.y = float(arg[1])
		self.z = float(arg[2])

	def set(self, val):
		if isinstance(val, self.__class__):
			self.x = val.x
			self.y = val.y
			self.z = val.z
		else:
			self.x = val[0]
			self.y = val[1]
			self.z = val[2]
		return self;

	def toString(self):
		return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

	def __mul__(self, other):
		if isinstance(other, self.__class__):
			return Vector((self.x * other.x, self.y * other.y, self.z * other.z))
		else:
			return Vector((self.x * other, self.y * other, self.z * other))

	def __rmul__(self, other):
		if isinstance(other, self.__class__):
			return Vector((self.x * other.x, self.y * other.y, self.z * other.z))
		else:
			return Vector((self.x * other, self.y * other, self.z * other))

	def __imul__(self, other):
		if isinstance(other, self.__class__):
			self.x *= other.x
			self.y *= other.y
			self.z *= other.z
		else:
			self.x *= other
			self.y *= other
			self.z *= other
		return self

	def __add__(self, other):
		if isinstance(other, self.__class__):
			return Vector((self.x + other.x, self.y + other.y, self.z + other.z))
		else:
			return Vector((self.x + other, self.y + other, self.z + other))

	def __radd__(self, other):
		if isinstance(other, self.__class__):
			return Vector((self.x + other.x, self.y + other.y, self.z + other.z))
		else:
			return Vector((self.x + other, self.y + other, self.z + other))

	def __iadd__(self, other):
		if isinstance(other, self.__class__):
			self.x += other.x
			self.y += other.y
			self.z += other.z
		else:
			self.x += other
			self.y += other
			self.z += other
		return self

	def toTuple(self):
		return (self.x, self.y, self.z)