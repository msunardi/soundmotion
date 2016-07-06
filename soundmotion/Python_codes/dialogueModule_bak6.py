import aiml
import speechd
import time
import os
import re
import threading
import sys

class Dialogue:

	def __init__(self):
		self.k = aiml.Kernel()
		self.k.learn("/home/msunardi/standard/std-hello.aiml")
		self.k.learn("/home/msunardi/standard/std-65percent.aiml")
		self.k.learn("/home/msunardi/standard/std-atomic.aiml")
		self.k.learn("/home/msunardi/standard/std-botmaster.aiml")
		self.k.learn("/home/msunardi/standard/std-brain.aiml")
		self.k.learn("/home/msunardi/standard/std-connect.aiml")
		self.k.learn("/home/msunardi/standard/std-dictionary.aiml")
		self.k.learn("/home/msunardi/standard/std-disconnect.aiml")
		self.k.learn("/home/msunardi/standard/std-dont.aiml")
		self.k.learn("/home/msunardi/standard/std-errors.aiml")
		self.k.learn("/home/msunardi/standard/std-gender.aiml")
		self.k.learn("/home/msunardi/standard/std-geography.aiml")
		self.k.learn("/home/msunardi/standard/std-german.aiml")
		self.k.learn("/home/msunardi/standard/std-gossip.aiml")
		self.k.learn("/home/msunardi/standard/std-inactivity.aiml")
		self.k.learn("/home/msunardi/standard/std-inventions.aiml")
		self.k.learn("/home/msunardi/standard/std-knowledge.aiml")
		self.k.learn("/home/msunardi/standard/std-lizards.aiml")
		self.k.learn("/home/msunardi/standard/std-login.aiml")
		self.k.learn("/home/msunardi/standard/std-numbers.aiml")
		self.k.learn("/home/msunardi/standard/std-personality.aiml")
		self.k.learn("/home/msunardi/standard/std-pickup.aiml")
		self.k.learn("/home/msunardi/standard/std-politics.aiml")
		self.k.learn("/home/msunardi/standard/std-profile.aiml")
		self.k.learn("/home/msunardi/standard/std-religion.aiml")
		self.k.learn("/home/msunardi/standard/std-robot.aiml")
		self.k.learn("/home/msunardi/standard/std-sales.aiml")
		self.k.learn("/home/msunardi/standard/std-sextalk.aiml")
		self.k.learn("/home/msunardi/standard/std-sports.aiml")
		self.k.learn("/home/msunardi/standard/std-srai.aiml")
		self.k.learn("/home/msunardi/standard/std-suffixes.aiml")
		self.k.learn("/home/msunardi/standard/std-that.aiml")
		self.k.learn("/home/msunardi/standard/std-turing.aiml")
		self.k.learn("/home/msunardi/standard/std-yesno.aiml")
		self.k.learn("/home/msunardi/standard/ext-commands.aiml")
		#self.k.learn("/home/msunardi/standard/ext-script1.aiml")
	#self.k.respond("load aiml b")
		try:
			self.client = speechd.SSIPClient('test')
		except:
			print "Well... no speech for now"
		#self.called = []
		try:
			self.facedetect = FaceDetect()
			self.facedetect.start()
		except:
			print "Well... I'm blind for now..."

	def youSay(self, inputstring):
		called = []
		input_text = str(inputstring)
		
		if input_text == 'exit()' or input_text == 'quit()':
			print "Exiting..."
			self.client.stop()
			self.client.close()
			exit()
			
		response = self.k.respond(input_text)
		try:
			self.client.speak(response)
		except:
			print "I'm having trouble speaking right now..."
		#self.client.speak(response, callback = lambda cb_type: called.append(cb_type))
		#while called.__contains__('end') == False:
		#	time.sleep(1)
		
		called = []
		try:
			if int(self.facedetect.faces) == 1:
				print "I see ", self.facedetect.faces, " face."
			elif int(self.facedetect.faces) > 1:
				print "I see ", self.facedetect.faces, " faces."
			else:
				print "I'm waiting..."
		except:
			print "..."

		return response
   
	def getValues(self, inputstring):
		return self.k.respond(inputstring) 

	def getFaces(self):
		return int(self.facedetect.faces)
		
	def recz(self):
		self.facedetect.toggleRecognize()
		return 1
	
	def getName(self):
		return self.facedetect.username()
	
	def say(self, sentence):
		try:
			self.client.speak(sentence)
		except:
			print "I'm having trouble speaking right now..."

class FaceDetect (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.faces = 0
		self.pattern = re.compile('There (is|are) (\d+) face? detected')
		self.pattern2 = re.compile('^Name: (\D*)\s')
		self.pattern3 = re.compile('^Closest match is (\D*) confidence?.$')
		self.pattern4 = re.compile('^posture: (\D*)\s')
		self.headx = re.compile('^head x: (\D*)\s')
		self.heady = re.compile('^head y: (\D*)\s')
		self.handx = re.compile('^hand x: (\-?\d*)\s')
		self.handy = re.compile('^hand y: (\-?\d*)\s')
		self.doRec = True
		self.name = None
		self.handgesture = None
		
		sys.path.append("/home/msunardi/Python-project/vision_tests")

	def doRecognize(self):
		self.doRec = True
		return self.doRec

	def toggleRecognize(self):
		self.doRec = not self.doRec
		return self.doRec
		
	def getHandGesture(self):
		return self.handgesture
	
	def username(self):
		if self.name is not None or self.name is not '':
			return self.name
		else:
			return False
				
	def run(self):
		print "Start facedetect"
		#(facedetect_in, facedetect_out) = os.popen2("python pyopencv-test5-facedetect.py")
		(facedetect_in, facedetect_out) = os.popen2("python vision_tests/visionModule.py")
		while True:
			if self.doRec:
				#print "recognizing..."
				vision_output = facedetect_out.readline()
				#print "Vision message: ", faces_detected
				match = self.pattern.match(vision_output)
				match2 = self.pattern2.match(vision_output)
				match3 = self.pattern3.match(vision_output)
				hand = self.pattern4.match(vision_output)
				headxmatch = self.headx.match(vision_output)
				headymatch = self.heady.match(vision_output)
				handxmatch = self.handx.match(vision_output)
				handymatch = self.handy.match(vision_output)
				
				if match:
					self.faces = match.group(2)
					print self.faces, "face detected!"
				if match2 and self.doRec:
					self.name = match2.group(1)
					print "Name:", self.name
					self.doRec = not self.doRec
				if match3:
					self.confidence = match3.group(1)
					print "Confidence:", self.confidence
				if hand:
					self.handgesture = hand.group(1)
					#if self.handgesture in ('Lpalm','Lback', 'victory', 'open', 'closed', 'sidepoint'):
					#	print "Hand gesture: %s" % (self.handgesture)
					if self.handgesture != '':
						print "Hand gesture: %s" % (self.handgesture)
					
				if headxmatch:
					print "Head x: ", headxmatch.group(1)
				if headymatch:
					print "Head y: ", headymatch.group(1)
					#print "Head position: %s, %s" % (headxmatch.group(1), headymatch.group(1))
				if handxmatch:
					handx = int(handxmatch.group(1))
					print "Hand x: ", handx,					
					
				if handymatch:
					handy = int(handymatch.group(1))
					print "Hand y: ", handy,
				
					#print "Hand position: %s, %s" % (handxmatch.group(1), handymatch.group(1))
				sys.stdout.flush()



#==================================
#		TEST
#==================================

if __name__== "__main__":
	facedetect = FaceDetect()
	facedetect.start()

"""
while True:
	input_text = raw_input("> ")	
	#response = self.k.respond(raw_input("> "))
	if input_text == 'exit()' or input_text == 'quit()':
		print "Exiting..."
		break
	response = self.k.respond(input_text)
	#print self.k.respond(raw_input("> "))
	print response
	print "I see ", facedetect.faces, " faces"
	client.speak(response, callback = lambda cb_type: called.append(cb_type))
	while called.__contains__('end') == False:
		time.sleep(2)
	called = []
	
client.stop()
client.close()
"""

