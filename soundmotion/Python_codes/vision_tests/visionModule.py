import sys
#sys.path.append("/home/msunardi/RoboLoco/RoboLoco_v02/features/vision/")
sys.path.append("/home/msunardi/experimental4/robolocovision/")

class pyVision:
	def __init__(self):
		import pyvision
		try:
			self.vision = pyvision.CVision()
		except: print "error loading CVision..."
		#self.vision.learnNew(True)
		self.facedetected = False
		self.faces = 0
		self.name = ''

	def recognizeUser(self):
		try:
			print "Recognizing..."
			#self.vision.recognize(True)
		except:
			print "visionModule.recognizeUser > recognize failed."
		try:
			print "Detecting face..."
			self.vision.detectfaces(True)
		except:
			print "visionModule.recognizeUser > detectfaces failed."
		
		#print "detected: ", self.vision.isFaceDetected()
		#print "faces: ", self.vision.returnNumberOfFaces()
		#print "Go go"
		#self.facedetected = self.vision.isFaceDetected()
		#self.faces = self.vision.returnNumberOfFaces()
		#self.name = self.vision.getName()
		print "Name: ", self.vision.getName()
		#print "Faces: ", self.vision.returnNumberOfFaces()
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
	
	def getConfidence(self):
		return self.vision.getConfidence()
		
if __name__ == "__main__":
	v = pyVision()
#	v.recognizeUser()
	c = 0
	facedetected = False
	def printPerson():
		print "Facedetected: ", facedetected, ";", faces, "faces detected!", ";", "Name: ", name
		sys.stdout.flush()

	while True:
		v.recognizeUser()
		print "ding", c
		c += 1
		
		"""if v.isFacedetected():
			facedetected = True
			faces = v.numberOfFaces()
			name = v.returnName()
			printPerson()	
			#var = raw_input("Press a key to continue...")
			#print "Name:", name
			#v.resetDetect()
			#sys.exit()
		else:
			facedetected = False
			faces = 0
			name = 'Unknown'
			printPerson()
			#var = raw_input("Press a key to continue...")

		v.resetDetect()
		facedetected = False"""


