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
	I = [(strong, light), (sudden, sustained), (direct, indirect), (bound, free)]
	
	return I

def ti (eff):
	return 0.5 + 0.4*max(eff[0][0], eff[2][0])-0.4*max(eff[0][1],eff[2][1]) + 0.8*min(eff[3][1],eff[0],[1])

def v0 (eff):
	return 0.1*eff[0][0] - max(.06*min(eff[2][1], eff[0][0]), .1*min(eff[3][1],eff[0][0]))

def v1 (eff):
	return max(.03*max(eff[0][1],eff[2][1]), (.2*eff[3][0]-.1*min(eff[1][1],eff[3][0])))

def texp (eff):
	return 1 + 2*eff[2][0] + (.2*min(eff[0][0],eff[2][0] - min(eff[3][0],eff[2][0]))) - .2*max(eff[0][0],min(eff[1][0],eff[2][1])) - .4*eff[3][0] - .5*min(eff[1][1],eff[3][0])

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

