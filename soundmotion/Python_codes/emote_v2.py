import math

def efforts(weight, time, space, flow):

	strong = light = direct = indirect = sudden = sustained = free = bound = 0
	if weight >= 0:
		strong = weight
		light = 1 - weight
	else:
		weight = abs(weight)		
		strong = 1 - weight
		light = weight
	
	if time >= 0:
		sudden = time
		sustained = 1 - time
	else:
		time = abs(time)
		sudden = 1 - time
		sustained = time	
	
	if space >= 0:
		direct = space
		indirect = 1 - space
	else:		
		space = abs(space)
		direct = 1 - space
		indirect = space
		
	if flow >= 0:
		bound = flow
		free = 1 - flow
	else:
		flow = abs(flow)
		bound = 1 - flow
		free = flow	
	I = {"weight": (strong, light), "time": (sudden, sustained), "space": (direct, indirect), "flow": (bound, free)}
	
	if I["weight"][0] > I["weight"][1]:
		print "strong",
	elif I["weight"][0] < I["weight"][1]:
		print "light",
	elif I["weight"][0] == I["weight"][1]:
		print "neutralweight",

	if I["time"][0] > I["time"][1]:
		print "sudden",
	elif I["time"][0] < I["time"][1]:
		print "sustained",
	elif I["time"][0] == I["time"][1]:
		print "neutraltime",

	if I["space"][0] > I["space"][1]:
		print "direct",
	elif I["space"][0] < I["space"][1]:
		print "indirect",
	elif I["space"][0] == I["space"][1]:
		print "neutralspace",

	if I["flow"][0] > I["flow"][1]:
		print "bound"
	elif I["flow"][0] < I["flow"][1]:
		print "free"
	elif I["flow"][0] == I["flow"][1]:
		print "neutralflow"
	
	return I

def ti (eff):
	return 0.5 + 0.4*max(eff["weight"][0], eff["time"][0]) - 0.4*max(eff["weight"][1],eff["time"][1]) + 0.8*min(eff["flow"][0],eff["weight"][1])

def v0 (eff):
	return 0.1*eff["weight"][0] - max(.06*min(eff["time"][1], eff["weight"][0]), .1*min(eff["flow"][1],eff["weight"][0]))

def v1 (eff):
	return max(.03*max(eff["weight"][1],eff["time"][1]), (.2*eff["flow"][1] - .1*min(eff["space"][1],eff["flow"][1])))

def texp (eff):
	return 1 + 2*eff["time"][0] + (.2*min(eff["weight"][0], eff["time"][0] - min(eff["flow"][1], eff["time"][0]))) - .2*max(eff["weight"][0], min(eff["space"][0], eff["time"][1])) - .4*eff["flow"][1] - .5*min(eff["space"][1], eff["flow"][1])

def elbow_angle (eff, current_angle, t_=None):
	if t_ is None:
		t_ = 0.5
	return current_angle * ( 1 + .4 * eff[1][1] * math.sin(2*math.pi*t_))

def t_ (frame_curr, key_next, key_prev):
	return (frame_curr - key_prev) / (key_next - key_prev)

def vt__ (t_, ti, v0, v1, texp):
	t0 = 0.01
	t1 = 0.99
	t__ = math.pow(t_, texp)
	if 0 <= t__ < t0:
		return -v0/t0*t__
	elif t0 <= t__ < ti:
		return ((v0 * ti) + (t0 * ti) - (v0 + ti) * t__)/(t0 - ti)
	elif ti <= t__ < t1:
		return ((v1 * ti) + (t1 * ti) - (v0 + ti) * t__)/(t1 - ti)
	elif t1 <= t__ <= 1:
		return (v1 * (1 - t__))/(t1 - 1)
	else:
		return 0

def hermiteInterpolate(y0, y1, y2, y3, mu, tension=None, bias=None):
	m0 = m1 = m2 = m3 = 0
	mu2 = mu * mu
	mu3 = m2 * mu

	if tension is None and bias is None:
		tension = 0
		bias = 0
	elif bias is None:
		bias = 0

	print tension, bias

	m0 = ((y1 - y0)*(1 + bias)*(1 - tension) + (y2 - y1)*(1 - bias)*(1 - tension))/2 
	m1 = ((y2 - y1)*(1 + bias)*(1 - tension) + (y3 - y2)*(1 - bias)*(1 - tension))/2
	a0 = 2*mu3 - 3*mu2 + 1
	a1 = mu3 - 2*mu2 + mu
	a2 = mu3 - mu2
	a3 = -2*mu3 + 3*mu2

	return a0*y1 + a1*m0 + a2*m1 + a3* y2