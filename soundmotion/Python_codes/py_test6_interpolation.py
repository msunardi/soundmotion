""" ================================
    Hermite Interpolation

    Parameters:
	y1	- start point of segment to interpolate
	y2	- end point of segment to interpolate
	y0	- one point before y1*
	y3	- one point after y2*
		*Hermite interpolation requires these extra points (y0, y3) to perform the interpolation between y1 & y2
	tension	- spline tension (-1: low, 0: normal, +1: high)
	bias	- spline bias (<0: towards y2, 0: even, >0: towards y1)

    Returns:
	a point between y1 and y2
    ===============================
"""

import math

def hermiteInterpolate(y0, y1, y2, y3, mu, tension=None, bias=None):
	#m0 = m1 = m2 = m3 = 0
	mu2 = mu * mu
	mu3 = mu2 * mu

	if tension is None and bias is None:
		tension = 0
		bias = 0
	elif bias is None:
		bias = 0

#	print tension, bias

	m0 = (y1 - y0)*(1 + bias)*(1 - tension)/2
	m0 += (y2 - y1)*(1 - bias)*(1 - tension)/2 
	m1 = (y2 - y1)*(1 + bias)*(1 - tension)/2
	m1 += (y3 - y2)*(1 - bias)*(1 - tension)/2
	a0 = 2*mu3 - 3*mu2 + 1
	a1 = mu3 - 2*mu2 + mu
	a2 = mu3 - mu2
	a3 = -2*mu3 + 3*mu2

	return (a0*y1) + (a1*m0) + (a2*m1) + (a3*y2)

""" ===============================
	TEST
    ===============================
"""

print "Hermite interpolation between P1 = 52, and P2 = 20"
print "Parameters:  s = 0.5, tension = 0, bias = 1"
print ""
print "P = ", hermiteInterpolate(41, 52, 20, 0, 0.5, 0, 1)
