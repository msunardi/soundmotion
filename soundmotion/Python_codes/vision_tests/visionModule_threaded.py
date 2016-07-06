import sys
import threading
sys.path.append("/home/msunardi/RoboLoco/RoboLoco_v02/features/vision/")

class pyVisionTh(threading.Thread):
	def __init__(self):
		import pyvision
		threading.Thread.__init__(self)
		self.vision = pyvision.CVision()
		#self.vision.learnNew(True)
		self.facedetected = False	
		self.faces = 0
		self.name = ''
		
	def recognizeUser(self):
		#print "Recognizing..."
		self.vision.recognize(True)
		self.vision.detectfaces(True)
		print "detected: ", self.vision.isFaceDetected()
		print "faces: ", self.vision.returnNumberOfFaces()
		print "Go go"
		self.facedetected = self.vision.isFaceDetected()
		self.faces = self.vision.returnNumberOfFaces()
		self.name = self.vision.getName()
		print "Name: ", self.vision.getName()
		print "Faces: ", self.vision.returnNumberOfFaces()
		"""while True:
			self.vision.detectfaces(True)
			if self.vision.isCentered():
				print "Face is centered."
			if self.vision.recognize(True):
				name = self.vision.getName()
				print "Hello, ", name, "."
			else:
				print "Sorry, I don't know you."
			break"""
		return True

	def returnName(self):
		return self.name
	
	def isFacedetected(self):
		return self.facedetected
	
	def numberOfFaces(self):
		return self.faces
	
	def resetDetect(self):	
		self.vision.resetDetect()
		#if __name__ == "__main__":
		#v = pyVision()
		#v.recognizeUser()
		#facedetected = False
	
	def printPerson(self):
		print "Facedetected: ", self.facedetected, ";", self.faces, "faces detected!", ";", "Name: ", self.name
		sys.stdout.flush()
		return self.facedetected, self.faces, self.name		
		
	def run(self):
		#v = pyVision()		# change all "v."'s to "self."
		#facedetected = False
		
		while True:
			self.recognizeUser()
			if self.isFacedetected() and self.facedetected is False:
				self.facedetected = True	#added "self." -- use global variable instead (7/13)
				self.faces = self.numberOfFaces()	#added "self." -- use global variable instead (7/13)
				self.name = self.returnName()	#added "self." -- use global variable instead (7/13)
				self.printPerson()
				#var = raw_input("Press a key to continue...")
				#print "Name:", name
				#v.resetDetect()
				#sys.exit()
			else:
				self.facedetected = False	#added "self." -- use global variable instead (7/13)
				self.faces = 0	#added "self." -- use global variable instead (7/13)
				self.name = 'Unknown'	#added "self." -- use global variable instead (7/13)
				#printPerson()
				#var = raw_input("Press a key to continue...")
			self.resetDetect()
			self.facedetected = False
			
if __name__ == "__main__":
	vmth = pyVisionTh()
	vmth.start()

\
