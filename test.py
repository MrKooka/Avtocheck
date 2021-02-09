class Poins:
	def set_coordinates(self,x,y):
		self.x = x
		self.y =y
	def get_distance(self,p2):
		x = p2.x - p1.x
		y = p2.y - p1.y
		return (x**2+y**2)**1/2
p1 = Poins()
p2 = Poins()
p1.set_coordinates(1, 2)
p2.set_coordinates(4, 6)
print(p1.get_distance(p2))
