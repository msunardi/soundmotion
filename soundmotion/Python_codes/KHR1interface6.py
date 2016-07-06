import sys

sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")

import KHR1Serial_test as KHR1Serial
import PyDebug
import threading, time

class khr1Interface (threading.Thread):

	def __init__(self, device, data=None):
		threading.Thread.__init__ (self)
		self.db = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
		self.serial = KHR1Serial.KHR1Serial(dbgobj=None)
		self.serial.Open(device)
		self.speed = 0x06
		self.data = data
		self.home0 = [0xee, 0x00, 0x00]
		self.home1 = [0xee, 0x01, 0x00]
		self.servodefaults = {'1': {'min':0, 'max':180, 'home':0},
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
							  '13':{'min':99, 'max':0, 'home':0},
							  '14':{'min':0, 'max':180, 'home':0},
							  '15':{'min':0, 'max':180, 'home':0},
							  '16':{'min':0, 'max':190, 'home':0},
							  '17':{'min':180, 'max':32, 'home':0},
							  '18':{'min':255, 'max':255, 'home':255},
							  '19':{'min':81, 'max':180, 'home':0},
							  '20':{'min':180, 'max':0, 'home':0},
							  '21':{'min':180, 'max':0, 'home':0},
							  '22':{'min':180, 'max':0, 'home':0},
							  '23':{'min':0, 'max':180, 'home':0},
							  '24':{'min':255, 'max':255, 'home':255}}
		self.killthread = False  

	def run(self):
		print "Running thread...",
		#threading.Thread(target=self.runMe(data)).start()
		while not self.killthread:
			if type(self.data).__name__ == 'list':
				self.runMe(self.data)
			elif type(self.data).__name__ == 'int':
				self.runMotion(self.data)
			elif type(self.data).__name__ == 'str':
				self.runScenario(self.data)
			else:
				print "I don't know what you're trying to do, but I don't like it."
			#self.runHome()
		print "thread is done."

	def runMe(self, data):
		print "Sending data..."
		for li in zip(*data):
			l = [0xfd, 0x00, self.speed]
			m = [0xfd, 0x01, self.speed]
			ch = 1
			for lo in li[:12]:
				"""if lo < 0:
					l+=[0x00]
				elif abs(lo-int(lo)) < 0.5:
					l+=[int(lo)]
				else:
					l+=[int(lo)+1]
				"""
				l += [self.cap(lo, ch)]
				ch = ch+1
				
			for le in li[12:]:
				m += [self.cap(le, ch)]
				ch = ch+1
			#print m

			#print "Out (float): ", li[0:12]
			#print "Out (int): ", l[3:len(l)]
			self.serial.SendCmd(l,2, 'ack')
			#time.sleep(0.5)
			#print "wait done."
			time.sleep(0.04)
			self.serial.SendCmd(m,2,'ack')
			time.sleep(0.04)
			if self.killthread:
				break
				
		self.killthread = True
		print "Data sent."

	def runMotion(self, data):
		print "Running motion #:", data
		l = [0xef, 0x00, data]
		if self.serial.SendCmd(l, 2, 'ack'):
			m = [0xef, 0x01, data]
			if self.serial.SendCmd(m, 2, 'ack'):
				print "Motion successfully executed."
				#if self.serial.SendCmd(self.home0, 2, 'ack'):
				#	self.serial.SendCmd(self.home1, 2, 'ack')

		else:
			print "There were some problems..."

	def runScenario(self, command):
		print "Running scenario...", command
		if command == 'dance':
			l = [0xee, 0x00, 0x01]
			if self.serial.SendCmd(l, 2, 'ack'):
				m = [0xee, 0x01, 0x01]
				self.serial.SendCmd(m, 2, 'ack')
		elif command == 'home':
			if self.serial.SendCmd(self.home0, 2, 'ack'):
				self.serial.SendCmd(self.home1, 2, 'ack')
		elif command == 'testspeed':
			self.testSpeed()

	def runHome(self):
		if self.serial.SendCmd(self.home0, 2, 'ack'):
			self.serial.SendCmd(self.home1, 2, 'ack')

	def cap(self, point, index):
		"""if index in [7,8,9,13,17,20,21,22]:
			max = self.servodefaults[str(index)]['min']
			min = self.servodefaults[str(index)]['max']
		else:
			max = self.servodefaults[str(index)]['max']
			min = self.servodefaults[str(index)]['min']
		"""
		max = self.servodefaults[str(index)]['max']
		min = self.servodefaults[str(index)]['min']
		home = self.servodefaults[str(index)]['home']
		
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
		"""if point < 0:
			return 0x00
		elif abs(point-int(point)) < 0.5:
			a = int(point)
		else:
			a = int(point)+1
		if a >= 180 and a != 225:
			return 0xb4
		else:
			return a"""

	def setSpeed(self, speed):
		print "Old speed: ", self.speed
		print "New speed: ", speed
		self.speed = speed
		
	def testSpeed(self):
		data = [[0,  0, 86, 225, 225,  90, 180, 180,  94, 225, 225, 225,  91, 133, 124,  98,  90, 225,  88,  51,  52,  90,  91, 225]]
		print "Sending data..."
		for li in data:
			l = [0xfd, 0x00, self.speed]
			ch = 1
			for lo in li[:12]:
				l += [self.cap(lo, ch)]
				ch = ch+1
			print "x"
			a = time.clock()
			#self.serial.SendCmd(l,2, 'ack')
			while not self.serial.SendCmd(l,2, 'ack'):
				pass
			b = time.clock()
			print "Ack: %f" % (b-a)
		self.togglethread()
		print "done."
		
		
	def togglethread(self):
		self.killthread = not self.killthread
		
if __name__ == "__main__":
	k = khr1Interface("/dev/ttyUSB0", "testspeed")
	k.start()
