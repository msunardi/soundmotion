#!/usr/bin/env python
#
#       emotionModule.py
#       
#       Copyright 2009 Mathias <msunardi@mbokjamu>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import numpy as np

class locoEmotion:
	
	def __init__(self):	
		self.emotion = {'happy': .25, 'fear': .25, 'sad': .25, 'anger': .25}
		"""paramMap matrix:
				rows (in order top-bottom): continuity, tension, bias, rate, highgain, medgain, lowgain
				columns (in order left-right): happy, fear, sad, anger
		"""				
		self.paramMap = np.matrix([[1.,-1.,1.,-1.],
								   [-1.,1.,.5,1.],
								   [-1.,.5,.5,-1.],
								   [1.,-1.,-1.,1.],
								   [-1.,1.,1.,-1.],
								   [1.,-1.,-1.,1.],
								   [1.,-1.,-1.,1.]])
		self.setEmoMatrix()
		self.resetEmo()
		
		
	def resetEmo(self):
		print "Resetting emo..."		
		self.emotion = {'happy': .25, 'fear': .25, 'sad': .25, 'anger': .25}
		self.alterEmo(0,0,0,0)
		self.probAction = 1
		self.intensity = 0
		#self.setEmoIntensity()
		#self.setEmoMatrix()		
		#self.updateFparamEmo()
		return 1
		
	def normalizeEmo(self):
		sum = float(self.emotion['happy']+self.emotion['fear']+self.emotion['sad']+self.emotion['anger'])
		self.emotion['happy'] /= sum
		self.emotion['fear'] /= sum
		self.emotion['sad'] /= sum
		self.emotion['anger'] /= sum
		
		return 1
	
	def setEmoMatrix(self):
		self.emoMatrix = np.matrix([[self.emotion['happy']],
									[self.emotion['fear']],
									[self.emotion['sad']],
									[self.emotion['anger']]])
									
	def setProbAction(self):
		self.probAction = self.emotion['happy'] + (.5*self.emotion['fear']) - (.5*self.emotion['sad']) - self.emotion['anger']
			
	def updateFparamEmo(self):
		self.newParam = self.paramMap * self.emoMatrix
		print "new emoparam:"
		print self.newParam
		
	def getEmoIntensity(self):		
		return self.intensity
	
	def setEmoIntensity(self):
		x = (self.emotion['fear'] - self.emotion['anger'])/4.
		y = (self.emotion['happy'] - self.emotion['sad'])/4.
		self.intensity = max(x,y)		
		
	def alterEmo(self, happy=0, fear=0, sad=0, anger=0):
		self.emotion['happy'] += happy
		self.emotion['fear'] += fear
		self.emotion['sad'] += sad
		self.emotion['anger'] += anger
		
		self.normalizeEmo()
		self.setProbAction()
		self.setEmoIntensity()
		self.setEmoMatrix()		
		self.updateFparamEmo()
		
	def getEmoParam(self):
		emoParam = [x[0,0] for x in self.newParam]
		# emoParam in order: [continuity, tension, bias, rate, highgain, medgain, lowgain]
		return (emoParam[0]+self.intensity)*3, (emoParam[1]+self.intensity)*3, (emoParam[2]+self.intensity)*3, max(1,emoParam[3]*7), emoParam[4], emoParam[5], emoParam[6]
	
	def getProbAction(self):		
		if self.probAction < 0:
			return 0
		else:
			return self.probAction
		
	def emoLevel(self, inputmatches):
		x = 0
		print "emoLevel>inputmatches:", inputmatches
		if inputmatches is not []:
			
			for i in inputmatches:
				if i[1]: x+=1
				elif i[2]: x+=1.5	#2
				elif i[3]: x+=2		#3
		print "Emolevel:", x
		return x
		
	def showEmos(self):
		return self.emotion
		
"""
def main():
	el = locoEmotion()
	matches = [('hate','','hate',''), ('dummy', '', '', 'dummy')]
	level = el.emoLevel(matches)
	el.alterEmo(1,0,2,3)
	print "probaction:", el.getProbAction()
	print "intensity:", el.getEmoIntensity()
	el.showEmos()
	#el.alterEmo(1,1,5,0)
	#print "probaction:", el.getProbAction()
	#print "intensity:", el.getEmoIntensity()
	#el.showEmos()
	
	(c,t,b,r,h,m,l) = el.getEmoParam()
	print "continuity: %f, tension: %f, bias: %f, rate: %d, highgain: %f, medgain: %f, lowgain: %f" % (c,t,b,r,h,m,l)
	
	el.resetEmo()			#reset emo parameters
	print "probaction:", el.getProbAction()
	print "intensity:", el.getEmoIntensity()
	el.showEmos()
	(c,t,b,r,h,m,l) = el.getEmoParam()
	print "continuity: %f, tension: %f, bias: %f, rate: %d, highgain: %f, medgain: %f, lowgain: %f" % (c,t,b,r,h,m,l)
	return 0

if __name__ == '__main__': main()
"""
