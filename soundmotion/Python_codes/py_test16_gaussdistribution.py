import math

class gauss:

    def __init__(self, a, b, c):

	self.f = lambda x: a*math.exp(-( pow(( x-b ),2)/(2* pow(c,2)) ))

    def degree(self, p):
	return self.f(p)

""" =========================
    test
    =========================
"""
eg = gauss(1, 6, 1)
print "gauss: a=1, b=4, c=1"
print "degree1= ", eg.degree(1) 
print "degree2= ", eg.degree(2)
print "degree4= ", eg.degree(4)
print "degree5= ", eg.degree(5)
print "degree6= ", eg.degree(6)
print "degree8= ", eg.degree(7)
