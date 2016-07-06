import sys
sys.path.append("/home/msunardi/RoboLoco/RoboLoco_v02/features/vision/")

class pyVision:
	def __init__(self):
		import pyvision
		self.vision = pyvision.CVision()
		#self.vision.learnNew(True)

	def recognizeUser(self):
		print "Recognize mode.  Recognizing..."
                self.vision.recognize(True)
                print "Name: ", self.vision.getName()
		#while True:
			#self.vision.detectfaces(True)
			#if self.vision.isCentered():
			#	print "Face is centered."
			#	if self.vision.recognize(True):
			#		name = self.vision.getName()
			#		print "Hello, ", name, "."
			#	else:
			#		print "Sorry, I don't know you."
			#	break


if __name__ == "__main__":
	v = pyVision()
	v.recognizeUser()
