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

import sys

sys.path.append("/home/msunardi/experimental4/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/experimental4/Fusion-0.10.2/Fusion/Utils")

import KHR1Serial_test as KHR1Serial
import KHR1CmdBase as KHR1Cmd
import PyDebug
import threading, time

DEVICE = "/dev/ttyUSB0"
defSpeed = 6
servoDefaults = {'1': {'min':0, 'max':180, 'home':0},
							  '2': {'min':0, 'max':180, 'home':0},
							  '3': {'min':0, 'max':180, 'home':0},
							  '4': {'min':255, 'max':255, 'home':255},
							  '5': {'min':255, 'max':255, 'home':255},
							  '6': {'min':0, 'max':180, 'home':0},
							  '7': {'min':0, 'max':180, 'home':0},
							  '8': {'min':0, 'max':180, 'home':0},
							  '9': {'min':0, 'max':180, 'home':0},
							  '10':{'min':255, 'max':255, 'home':255},
							  '11':{'min':255, 'max':255, 'home':255},
							  '12':{'min':255, 'max':255, 'home':255},
							  '13':{'min':9, 'max':-90, 'home':0},
							  '14':{'min':51, 'max':-129, 'home':0},
							  '15':{'min':-125, 'max':55, 'home':0},
							  '16':{'min':-90, 'max':90, 'home':0},
							  '17':{'min':90, 'max':-32, 'home':0},
							  '18':{'min':255, 'max':255, 'home':255},
							  '19':{'min':-19, 'max':90, 'home':0},
							  '20':{'min':-51, 'max':129, 'home':0},
							  '21':{'min':125, 'max':-55, 'home':0},
							  '22':{'min':90, 'max':-90, 'home':0},
							  '23':{'min':-90, 'max':30, 'home':0},
							  '24':{'min':255, 'max':255, 'home':255}}
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
				print "runScenario"
				if self.data == 'testinc':
					self.incPos()
			else:
				print "I don't know what you're trying to do, but I don't like it."
		
		print "thread is done."
	
	def runMe(self, data, speed=defSpeed):
		try:
			new_data = self.convertData(data)
			print "runMe...", len(new_data)
			#print "new_data:", new_data
			for step in zip(*new_data):
				#print "step=", step, "length:", len(step)
				#step = self._GroomChannelList(step)
				#print "new step=", step
				# use these two when the speed is included in the data [0]
				#self.CmdSetCurPos(step[0], step[1:])	#<<< method inherited from KHR1Cmd
				#while self.CmdGetCurPos() != step[1:]:	#<<< method inherited from KHR1Cmd
				self.CmdSetCurPos(defSpeed, step)				
				#self.RCB1CmdSetCurPos(0, defSpeed, step[:12])
				#while self.CmdGetCurPos() != step:
				# wait until position is done...
					#self.CmdSetCurPos(defSpeed, step)
					#print "Ack: %d" % (KHR1Serial.ACK)
				time.sleep(0.04)
				if self.killthread:
					break
					
			self.killthread = True
			return 1
		except:
			print "Motion data execution failed."
	
	def runMotion(self, motion_number):
		try:
			self.CmdPlayMotion(motion_number)
			return 1
		except:
			print "Play motion failed."
			return 0
	
	def runScenario(self, scenario_number):
		try:
			self.CmdPlayScenario(scenario_number)
			return 1
		except:
			print "Play scenario failed."
			return 0
			
	def incPos(self, data=None):
		self.CmdSetIncCurPos(3, neck=150, lshoulder=100)
		self.CmdSetIncCurPos(5, lshoulder=120)
	
	def convertData(self, data):
		litmp = []		
		for li in data:
			lotmp = []
			ch = 1
			lotmp = [[int(i) for i in li]]
			litmp += lotmp
		return litmp
		
	def cap(self, point, index):	
		
		max = servoDefaults[str(index)]['max']
		min = servoDefaults[str(index)]['min']
		home = servoDefaults[str(index)]['home']
		
		if abs(point - int(point)) < 0.5: #if the value is fractional...
			a = int(point)	# if the the fraction is < 0.5, round down...
		else:
			a = int(point)+1	# if the fraction is >= 0.5, round up.
			
		if a < min:			# if the calculated point is less than the min...
			return min	# use the min value...
		elif a > max:		# or, if the point is more than the max...
			return max	# use the max value...
		else:
			return a		# otherwise, return the point
		
	def togglethread(self):
		self.killthread = not self.killthread

def main():
	
	ki = khr1Interface(data=[[90 for i in range(24)]])
	#ki = khr1Interface(data='testinc')
	#ki = khr1Interface(data=29)
	ki.start()
	return 0

if __name__ == '__main__': main()
