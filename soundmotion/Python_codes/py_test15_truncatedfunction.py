import math

g = lambda x: 0.5*x+2

print g(2)

#---- lambda function in a list

list = [g]

print list[0](2)

h = lambda x: g(2)*x

list.append(h)

print list[1](1)

j = lambda x: 1

print j(100)

print .1/4*10

class truncated:

    def __init__(self,p1, p2, p3, p4):
	self.a = .1/p2*10
	self.b = -.1/abs(p4-p3)*10
    
	self.f0 = lambda x: self.a*x
        self.f1 = lambda x: 1
	self.f2 = lambda x: self.b*x+1
	
        self.r0 = p1
	self.r1 = p2
	self.r2 = p3
	self.r3 = p4

    def degree(self, p):
	if self.r0 <= p < self.r1:
	    return self.f0(p)
	elif self.r1 <= p <= self.r2:
	    return self.f1(p)
        elif self.r2 < p <= self.r3:
	    return self.f2(p-self.r2)

""" =========================
    test
    =========================
"""
eg = truncated(0, 4, 6, 10)
print "Truncated: points(0, 4, 6, 10)" 
print "degree2= ", eg.degree(2)
print "degree4= ", eg.degree(4)
print "degree5= ", eg.degree(5)
print "degree6= ", eg.degree(6)
print "degree8= ", eg.degree(8)
