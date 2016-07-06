"""======================================
Cognition model:

personalityMatrix * functionMatrix = behaviorMatrix

personalityMatrix:
--Describes the expression of behaviors; the relationship between behaviors and their corresponding signal transformation functions
	col (functions): interpolation, sampling, gains, waveshape, motionBlend(superpose), selfAwareness
	row (behaviors): Base, Anticipation, Exaggeration, Overlap/Follow-through, StretchnSquash, Time(ing), Weight, Space, Flow, Tired, Energetic, LowEmo, HiEmo, Shaking

functionMatrix:
--Parameters of signal transformation functions
   col:	interpolation(data, bias, tension, continuity) (kbInterpolation),
		sampling(rate),
		gains(lowGains, medGains, hiGains),
		waveshape(function (expressions), (points, values)),
		motionBlend(motion1, motion2).
		selfAwareness(orientation, target) # not implemented yet

========================================"""

import numpy as np

class Cognition:
	
	def __init__(self):
		self.pMatrix = None		#personality Matrix
		self.fMatrix = None		#function Matrix
		self.model1()
		self.defFunct()

	def model1(self):
		self.pMatrix = np.matrix('.5,0,0,0,0,0; 1,0,0,1,0,1; 0,0,1,1,0,0; 1,0,0,0,0,0; 1,0,.5,0,0,1; 1,1,0,0,0,0; 1,0,1,1,1,0; 0,0,0,0,0,1; 1,0,1,0,0,0; 1,0,1,0,1,0; 0,0,0,1,0,0; 1,1,1,0,1,0; 1,0,1,0,1,0; 0,1,1,.5,1,0')

	def defFunct(self):
		#self.fMatrix = {'interpolation':[0,0,0], 'sampling':[0], 'gains': [0,0,0], 'waveshape':[None, None], 'motionBlend':[None, None], 'selfAwareness': [1,0,0,0,0,0]}
		self.fMatrix = [[9],[2],[8],[10],[12],[15]]

	def printModel(self):
		print "Personality Matrix:", self.pMatrix
		print "Function Matrix:", self.fMatrix
		print "pMatrix x fMatrix =", self.pMatrix*self.fMatrix



if __name__=="__main__":
	y = Cognition()
	y.printModel()
								  
