import math
import numpy

def hermiteInterpolate(y0, y1, y2, y3, mu, tension=0, bias=0, continuity=None):
	m0 = m1 = 0
	mu2 = mu * mu
	mu3 = mu2 * mu

	"""if tension is None and bias is None:
		tension = 0
		bias = 0
	elif bias is None:
		bias = 0
        """
#	print tension, bias

	m0 = ((y1 - y0)*(1 + bias)*(1 - tension) + (y2 - y1)*(1 - bias)*(1 - tension))/2 
	m1 = ((y2 - y1)*(1 + bias)*(1 - tension) + (y3 - y2)*(1 - bias)*(1 - tension))/2
	a0 = 2*mu3 - 3*mu2 + 1
	a1 = mu3 - 2*mu2 + mu
	a2 = mu3 - mu2
	a3 = -2*mu3 + 3*mu2

	return a0*y1 + a1*m0 + a2*m1 + a3* y2

def kbInterpolate(y0, y1, y2, y3, mu, tension=0, bias=0, continuity=0): # Kochanek-Bartels variant of Hermite
	m0 = m1 = 0
	mu2 = mu * mu
	mu3 = mu2 * mu
	
	"""if tension is None and bias is None:
		tension = 0
		bias = 0
	elif bias is None:
		bias = 0
        """
#	print tension, bias

	TS = ((y2 - y1)*(1 + bias)*(1-continuity)*(1 - tension) + (y3 - y2)*(1 - bias)*(1+continuity)*(1 - tension))/2 
	TD = ((y1 - y0)*(1 + bias)*(1+continuity)*(1 - tension) + (y2 - y1)*(1 - bias)*(1-continuity)*(1 - tension))/2
	"""a0 = 2*mu3 - 3*mu2 + 1
	a1 = mu3 - 2*mu2 + mu
	a2 = mu3 - mu2
	a3 = -2*mu3 + 3*mu2
        """
	h = numpy.matrix([[ 2, -2,  1,  1],
                          [-3,  3, -2, -1],
                          [ 0,  0,  1,  0],
                          [ 1,  0,  0,  0]], dtype=float)
	C = numpy.matrix([[y1], [y2], [TD], [TS]])
	S = numpy.array([[mu3, mu2, mu, 1]])
	result = S*h*C	
        #print type(result)
	return result

def linearInterpolate(y1, y2, mu):
	return (y1*(1-mu) + y2*mu)
