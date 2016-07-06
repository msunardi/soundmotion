import math

class emote:

    def __init__ (self):
        self.I= {}
        pass

    def efforts(self, weight, time, space, flow):

	self.strong = self.light = self.direct = self.indirect = self.sudden = self.sustained = self.free = self.bound = 0
	
	"""  EFFORT - WEIGHT parameter:
		if > 0 then STRONG
		if < 0 then LIGHT
		if = 0 then NEUTRAL
	"""
        self.strong = weight
        self.light = 0 - weight

	"""  EFFORT - TIME parameter:
		if > 0 then SUDDEN
		if < 0 then SUSTAINED
		if = 0 then NEUTRAL
	"""
        self.sudden = time
        self.sustained = 0 - time

	"""  EFFORT - SPACE parameter:
		if > 0 then DIRECT
		if < 0 then INDIRECT
		if = 0 then NEUTRAL
	"""
        self.direct = space
        self.indirect = 0 - space
		
	""" EFFORT - FLOW parameter:
		if > 0 then BOUND
		if < 0 then FREE
		if = 0 then NEUTRAL
	"""	
        self.bound = flow
        self.free = 0 - flow
		

        self.I = {"weight": (self.strong, self.light), "time": (self.sudden, self.sustained), "space": (self.direct, self.indirect), "flow": (self.bound, self.free)}
        print "Weight: ",	
        if self.I["weight"][0] > self.I["weight"][1]:
            print "strong"
        elif self.I["weight"][0] < self.I["weight"][1]:
            print "light"
        elif self.I["weight"][0] == self.I["weight"][1]:
        #elif I["weight"][0] == 0:
            print "neutralweight"

        print "Time: ",
        if self.I["time"][0] > self.I["time"][1]:
            print "sudden"
        elif self.I["time"][0] < self.I["time"][1]:
            print "sustained"
        elif self.I["time"][0] == self.I["time"][1]:
        #elif I["time"][0] == 0:
            print "neutraltime"

        print "Space: ",
        if self.I["space"][0] > self.I["space"][1]:
            print "direct"
        elif self.I["space"][0] < self.I["space"][1]:
            print "indirect"
        elif self.I["space"][0] == self.I["space"][1]:
        #elif I["space"][0] == 0:
            print "neutralspace"

        print "Flow: ",
        if self.I["flow"][0] > self.I["flow"][1]:
            print "bound"
        elif self.I["flow"][0] < self.I["flow"][1]:
            print "free"
        elif self.I["flow"][0] == self.I["flow"][1]:
        #elif I["flow"][0] == 0:
            print "neutralflow"
	
        return self.I

    def ti (self, eff):
        return 0.5 + 0.4*max(eff["weight"][0], eff["time"][0]) - 0.4*max(eff["weight"][1],eff["time"][1]) + 0.8*min(eff["flow"][0],eff["weight"][1])

    def v0 (self, eff):
        return 0.1*eff["weight"][0] - max(.06*min(eff["time"][1], eff["weight"][0]), .1*min(eff["flow"][1],eff["weight"][0]))

    def v1 (self, eff):
        return max(.03*max(eff["weight"][1],eff["time"][1]), (.2*eff["flow"][1] - .1*min(eff["space"][1],eff["flow"][1])))

    def texp (self, eff):
        return 1 + 2*eff["time"][0] + (.2*min(eff["weight"][0], eff["time"][0] - min(eff["flow"][1], eff["time"][0]))) - .2*max(eff["weight"][0], min(eff["space"][0], eff["time"][1])) - .4*eff["flow"][1] - .5*min(eff["space"][1], eff["flow"][1])

    def elbow_angle (self, eff, current_angle, t_=None):
        if t_ is None:
             t_ = 0.5
        return current_angle * ( 1 + .4 * eff["space"][1] * math.sin(2*math.pi*t_))

    def t_ (frame_curr, key_next, key_prev):
        return (frame_curr - key_prev) / (key_next - key_prev)

    def vt__ (self, t_, ti, v0, v1, texp):
        self.t0 = 0.01
        self.t1 = 0.99
        self.t__ = math.pow(t_, texp)
        if 0 <= self.t__ < self.t0:
            return -v0/self.t0*self.t__
        elif self.t0 <= self.t__ < ti:
            return ((v0 * ti) + (self.t0 * ti) - (v0 + ti) * self.t__)/(self.t0 - ti)
        elif ti <= self.t__ < self.t1:
            return ((v1 * ti) + (self.t1 * ti) - (v0 + ti) * self.t__)/(self.t1 - ti)
        elif self.t1 <= self.t__ <= 1:
            return (v1 * (1 - self.t__))/(self.t1 - 1)
        else:
            return 0

    def hermiteInterpolate(self, y0, y1, y2, y3, mu, tension=None, bias=None):
        self.m0 = self.m1 = self.m2 = self.m3 = 0
        self.mu2 = mu * mu
        self.mu3 = self.m2 * mu

        if tension is None and bias is None:
            tension = 0
            bias = 0
        elif bias is None:
            bias = 0

        print tension, bias

        self.m0 = ((y1 - y0)*(1 + bias)*(1 - tension) + (y2 - y1)*(1 - bias)*(1 - tension))/2 
        self.m1 = ((y2 - y1)*(1 + bias)*(1 - tension) + (y3 - y2)*(1 - bias)*(1 - tension))/2
        self.a0 = 2*self.mu3 - 3*self.mu2 + 1
        self.a1 = self.mu3 - 2*self.mu2 + mu
        self.a2 = self.mu3 - self.mu2
        self.a3 = -2*self.mu3 + 3*self.mu2

        return self.a0*y1 + self.a1*self.m0 + self.a2*self.m1 + self.a3* y2


"""  ==================================
	TEST
     ==================================
"""
"""
print "Weight = -0.8, Time = 1, Space = 0, Flow = -1"
Em = emote()
J = Em.efforts(-0.8,1,0,-1)
in_ti = Em.ti(J)
in_v0 = Em.v0(J)
in_v1 = Em.v1(J)
in_texp = Em.texp(J)
in_elbow_angle = Em.elbow_angle(J, math.pi/5)
in_vt__ = Em.vt__(0.5, in_ti, in_v0, in_v1, in_texp)


print ""
#print J
print "ti= ", in_ti,"| v0= ", in_v0, "| v1= ", in_v1, "| texp= ", in_texp
print "elbow_angle= ", in_elbow_angle, "| vt__= ", in_vt__
"""
