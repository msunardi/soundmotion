#!/usr/bin/env python
#
#       LocoKHR1Interface.py
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
#
#	v5: fixed the min-max-home positions

import sys

#sys.path.append("/home/msunardi/experimental4/Fusion-0.10.2/Fusion/KHR1/Cmd")
#sys.path.append("/home/msunardi/experimental4/Fusion-0.10.2/Fusion/Utils")

#import KHR1Serial_test2 as KHR1Serial
import KHR1CmdBase as KHR1Cmd
import PyDebug
import threading, time, random

DEVICE = "/dev/ttyUSB0"
defSpeed = 5
servoDefaults = {'1': {'min':0, 'max':180, 'home':0},
				 '2': {'min':0, 'max':180, 'home':0},
				 '3': {'min':0, 'max':180, 'home':0},
				 '4': {'min':255, 'max':255, 'home':255},
				 '5': {'min':255, 'max':255, 'home':255},
				 '6': {'min':0, 'max':180, 'home':0},
				 '7': {'min':180, 'max':0, 'home':180},
				 '8': {'min':180, 'max':0, 'home':180},
				 '9': {'min':17, 'max':180, 'home':107},
				 '10':{'min':255, 'max':255, 'home':255},
				 '11':{'min':255, 'max':255, 'home':255},
				 '12':{'min':255, 'max':255, 'home':255},
				 '13':{'min':0, 'max':100, 'home':91},	# range 90 to -90 (180 to 0)
				 '14':{'min':0, 'max':180, 'home':129},	# range 51 to -129 (0 to 180)
				 '15':{'min':0, 'max':180, 'home':125}, # range -125 to 55 (0 to 180)
				 '16':{'min':0, 'max':180, 'home':90}, # range -90 to 90 (0 to 180)
				 '17':{'min':58, 'max':180, 'home':90}, # range 90 to -90 (180 to 0) (limit: 90 to -32 (180 to 32))
				 '18':{'min':255, 'max':255, 'home':255}, 
				 '19':{'min':74, 'max':180, 'home':88}, # range -90 to 90 (0 to 180) (limit: -19 to 90 (81 to 180))
				 '20':{'min':180, 'max':0, 'home':51}, # range -51 to 129 (180 to 0)
				 '21':{'min':180, 'max':0, 'home':55}, # range 125 to -55 (180 to 0)
				 '22':{'min':180, 'max':0, 'home':90}, # range 90 to -90 (180 to 0)
				 '23':{'min':120, 'max':0, 'home':90}, # range -90 to 90 (0 to 180) (limit: -90 to 30 (0 to 120))
				 '24':{'min':255, 'max':255, 'home':255}}
clock = 0.066666666666
delay = {'7':3, '6':1.7, '5':.5, '4':.2, '3':.2, '2':.2, '1':.2, '0':.2}

class khr1Interface (threading.Thread, KHR1Cmd.KHR1CmdBase):

	def __init__(self, device=DEVICE, data=None):
		threading.Thread.__init__ (self)
		KHR1Cmd.KHR1CmdBase.__init__(self,port=device, boardIdList=KHR1Cmd.KHR1BoardIdListDft,
                    servoVersion=KHR1Cmd.KHR1ServoVersionDft,
                    activeServos=KHR1Cmd.KHR1FacDftActiveServos)
		self.data = data
		self.killthread = False
		
		#print self.AttrGetActiveServos()
		#self.mNumOfChannels = 24
	
	def run(self):
		print "Running KHR1Interface thread...",
		#threading.Thread(target=self.runMe(data)).start()
		while not self.killthread:
			if type(self.data).__name__ == 'list':
				#self.runMe(self.data)
				print "runMe"#, self.data, len(self.data[0])
				self.runMe(self.data)
			elif type(self.data).__name__ == 'int':
				self.runMotion(self.data)
				print "runMotion"
			elif type(self.data).__name__ == 'str':
				#self.runScenario(self.data)
				print "runScenario", self.data
				if self.data == 'testinc':
					self.incPos()
				elif self.data == 'gettrim':
					self.getTrim()
				elif self.data == 'testspeed':
					self.testSpeed()
				elif self.data == 'dance':
					self.runScenario(1)
				elif self.data in ['happy','sad','anger','fear']:
					self.setPose(self.data)
				elif self.data == 'greet':
					self.runMotion(2)
			else:
				print "I don't know what you're trying to do, but I don't like it."
		
		print "thread is done."
	
	def setPose(self, data):
		try:
			if data == 'happy':
				self.runMotion(32)
			elif data == 'fear':
				self.runMotion(31)
			elif data == 'sad':
				self.runMotion(30)
			elif data == 'anger':
				self.runMotion(29)
		except:
			print "locoKHR1Interface_v8: setPose() failed."
	
	def runMe(self, data, speed=5):
		print "runMe..."
		try:
			new_data = self.convertData(data)
			print "runMe...", len(new_data)
			#print "new_data:", new_data
			#clock = 0.066666666666
			
			#sleep = (speed*clock)+(random.randrange(1,3)*.0015)
			#print "sleep = %f" % sleep
			#print "speed = %d" % speed
			i = 0
			l = len(new_data[0])
			sleepdata = []
			ndata = zip(*new_data)
			j=0
			for snap in ndata:
				if j < (l-1):
					diff = max(map(lambda x,y:abs(y-x),snap, ndata[j+1]))
					sleepdata += [self.getSleep(speed, diff)]
				#print diff
				j += 1
			#print "sleepdata:", sleepdata
			i = 0
			for step in ndata:
				#print "step=", step, "length:", len(step)
				#step = self._GroomChannelList(step)
				#print "new step=", step
				# use these two when the speed is included in the data [0]
				#self.CmdSetCurPos(step[0], step[1:])	#<<< method inherited from KHR1Cmd
				#while self.CmdGetCurPos() != step[1:]:	#<<< method inherited from KHR1Cmd
				#self.CmdSetCurPos(speed, step)				
				self.RCB1CmdSetCurPos(0, speed, step[:12])
				self.RCB1CmdSetCurPos(1, speed, step[12:])
				#while self.CmdGetCurPos() != step:
				# wait until position is done...
					#self.CmdSetCurPos(defSpeed, step)
					#print "Ack: %d" % (KHR1Serial.ACK)
				#if i < (l-1):
					#print "i: %d, l: %d" % (i,l)
				#	diff = max(map(lambda x,y:abs(y-x),step, ndata[i+1]))
				#	print "cur vs next:", diff
					#sleep = (speed*clock)+(random.randrange(1,3)*.0015)
				#	sleep = self.getSleep(speed,diff)
				time.sleep(0.01)
				#if i < (l-1):
				#	time.sleep(sleepdata[i])
				if self.killthread:
					break
				i += 1
					
			self.killthread = True
			return 1
		except:
			print "Motion data execution failed."
	
	def getSleep(self,speed,diff):
		clock = 0.00005
		if diff > 100:	# if the movement is 90 degrees or more -- give more delay
			sleep = (speed*clock)+delay[str(speed)]
			#sleep = (speed*clock)+(random.randrange(1,3)*.0015)
		else:
			sleep = (speed*clock)+(random.randrange(1,3)*.0015)
		#print "sleep = %f" % sleep
		#print "speed = %d" % speed
		return sleep
	
	def runMotion(self, motion_number):
		try:
			self.CmdPlayMotion(motion_number)
			self.killthread = True
			return 1
		except:
			print "Play motion failed."
			return 0
	
	def runScenario(self, scenario_number):
		try:
			self.CmdPlayScenario(scenario_number)
			self.killthread = True
			return 1
		except:
			print "Play scenario failed."
			return 0
			
	def incPos(self, data=None):
		self.CmdSetIncCurPos(3, neck=150, lshoulder=100)
		self.CmdSetIncCurPos(5, lshoulder=120)
		
	def getTrim(self):
		print "Trim:", self.CmdGetTrim()
		self.togglethread()
	
	def convertData(self, data):
		litmp = []
		ch = 1
		print "converting..."
		for li in data:
			#lotmp = []
			
			#lotmp = [[int(i) for i in li]]
			#for j in [13,16,19,21]:
			#	lotmp[0][j] = servoDefaults[str(j+1)]['home']
				#print servoDefaults[str(j+1)]['home']
			#litmp += lotmp
			#if ch in [13,16,19,21]:
			#	litmp += [[servoDefaults[str(ch)]['home'] for i in li]]
			#else:
			#	litmp += [[int(i) for i in li]]
			litmp += [[int(i) for i in li]]
			#litmp += [[self.cap(i,ch) for i in li]]
			#l = [[self.adjustData(ch,i) for i in li]]
			#litmp += l
			#print "li:", li
			#print "l:", l
			ch +=1
		return litmp
		
	def cap(self, point, index):	
		
		max = servoDefaults[str(index)]['max']
		min = servoDefaults[str(index)]['min']
		home = servoDefaults[str(index)]['home']
		
		if abs(point) - abs(int(point)) < 0.5: #if the value is fractional...
			a = int(point)	# if the the fraction is < 0.5, round down...
		else:
			if point < 0:
				a = int(point) - 1
			else:
				a = int(point)+1	# if the fraction is >= 0.5, round up.
			
		if a < min:			# if the calculated point is less than the min...
			return min	# use the min value...
		elif a > max:		# or, if the point is more than the max...
			return max	# use the max value...
		else:
			return a		# otherwise, return the point

	#def adjustData(self, id, point): #<< moved to KHR1Readcsv.py (called by mosynth##_p.py)
		"""if id == 3 or id == 6 or id == 16:
			if point < -90:	return 0
			elif point > 90: return 180
			else: return point + 90		
		elif id == 7 or id == 8:
			if point > 0: return 180
			elif point < -180: return 0
			else: return point + 180
		elif id == 9:
			if point > 90: return 180
			elif point < -90: return 0
			else: return point + 90
		elif id == 13:
			if point > 9: return 99
			elif point < -90: return 0
			else: return point + 90
		elif id == 14:
			if point > 51: return 180
			elif point < -129: return 0
			else: return point + 129
		elif id == 15:
			if point < -125: return 0
			elif point > 55: return 180
			else: return point + 125
		#elif id == 16:
		#	if point < -90:	return 0
		#	elif point > 90: return 180
		#	else: return point + 90
		elif id == 17:
			if point > 90: return 180
			elif point < -32: return 32
			else: return point + 90
		elif id == 19:
			if point < -19:	return 81
			elif point > 90: return 180
			else: return point + 90
		elif id == 20:
			if point < -51: return 0
			elif point > 129: return 180
			else: return point + 51
		elif id == 21:
			if point > 125:	return 180
			elif point < -55: return 0
			else: return point + 55
		elif id == 22:
			if point > 90: return 180
			elif point < -90: return 0
			else: return point + 90
		elif id == 23:
			if point < -90:	return 0
			elif point > 30: return 120
			else: return point + 90
		else: return point	"""		
		
	def togglethread(self):
		self.killthread = not self.killthread
	
	# - test function to measure speed vs. sleep (timing)
	def testSpeed(self):
		"""data = [[0,  0, 86, 225, 225,  90, 180, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90,  45, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90, 180, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90,  45, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90, 180, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90,  45, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90, 180, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90,  45, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90, 180, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90,  45, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90, 180, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225],
				[0,  0, 86, 225, 225,  90,  45, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225]]
		"""
		data = [[0,  0, 86, 225, 225,  90,  50, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[25,  0, 86, 225, 225,  90,  55, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[75,  0, 86, 225, 225,  90,  60, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[150,  0, 86, 225, 225,  90,  65, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[160,  0, 86, 225, 225,  90,  70, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[165,  0, 86, 225, 225,  90,  75, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[167,  0, 86, 225, 225,  90,  80, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[165,  0, 86, 225, 225,  90,  85, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[150,  0, 86, 225, 225,  90,  90, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[75,  0, 86, 225, 225,  90,  95, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[25,  0, 86, 225, 225,  90, 100, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225],
				[0,  0, 86, 225, 225,  90, 105, 180,  94, 225, 225, 225,  91, 129, 124,  90,  90, 225,  88,  51,  52,  90,  90, 225]]
		data = self.convertData(data)
		print "Sending data..."
		#clock = 0.066666666666
		clock = 0.00005
		#sleep = 0.033333333
		spd = 5
		#sleep = (spd*clock)+(random.randrange(1,3)*.0015)		
		sleep = (spd*clock)+0.002
		print "sleep = %f" % sleep
		print "speed = %d" % spd
		#for i in range(10):
		for li in data:
			#li = data[0]
			#l = [0xfd, 0x00, 0x05]
			#ch = 1
			
			#for lo in li[:12]:
			#	l += [self.cap(lo, ch)]
			#	ch = ch+1
			#print "x"
			#-a = time.time()
			#self.serial.SendCmd(l,2, 'ack')
			#self.SendCmd(l,2,None)
			#self.CmdSetCurPos(spd, li)
			self.RCB1CmdSetCurPos(0, spd, li[:12])
			#print "c", c
			##	pass
			self.RCB1CmdSetCurPos(1, spd, li[12:])
			time.sleep(1)
			#-rint li[:12]
			#-print self.RCB1CmdGetCurPos(0)
			#while self.RCB1CmdGetCurPos(0) != li:
			#	print "current position:", self.RCB1CmdGetCurPos(0)
			#	print "li:", li
			#	self.RCB1CmdSetCurPos(0, defSpeed, li[:12])
			
			
			#-b = time.time()
			#-print "Delay: %f" % ((b-a))
		self.togglethread()
		print "done."

def main():
	
	#ki = khr1Interface(data=[[90 for i in range(24)]])
	#ki = khr1Interface(data='testinc')
	#ki = khr1Interface(data=29)
	#ki = khr1Interface(data='gettrim')
	#ki = khr1Interface(data='testspeed')
	ki = khr1Interface(data='dance')
	ki.start()
	
	return 0

if __name__ == '__main__': main()
