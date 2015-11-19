import math

def Sprial_Waypoint_Generator_xy( DistanceBetweenTurn, DistanceBetweenPoints):

	a = DistanceBetweenTurn / math.pi
	r = a * theta									# formula of  spiral
	
	for i in range(0, 100):
		theta = i * (2 * math.pi / 100)
		r = a * theta
		x = r * math.cos(theta)						# polar to xy
		y = r * math.sin(theta)						# polar to xy
		print "("+str(x)+", "+str(y)+")\n"
	