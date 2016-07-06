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
        #self.k.learn("/home/msunardi/standard/std-atomic.aiml")
        #self.k.learn("/home/msunardi/standard/std-botmaster.aiml")
        #self.k.learn("/home/msunardi/standard/std-brain.aiml")
        #self.k.learn("/home/msunardi/standard/std-connect.aiml")
        #self.k.learn("/home/msunardi/standard/std-dictionary.aiml")
        #self.k.learn("/home/msunardi/standard/std-disconnect.aiml")
        #self.k.learn("/home/msunardi/standard/std-dont.aiml")
        #self.k.learn("/home/msunardi/standard/std-errors.aiml")
        #self.k.learn("/home/msunardi/standard/std-gender.aiml")
        #self.k.learn("/home/msunardi/standard/std-geography.aiml")
        #self.k.learn("/home/msunardi/standard/std-german.aiml")
        self.k.learn("/home/msunardi/standard/std-gossip.aiml")
        #self.k.learn("/home/msunardi/standard/std-inactivity.aiml")
        self.k.learn("/home/msunardi/standard/std-inventions.aiml")
        self.k.learn("/home/msunardi/standard/std-knowledge.aiml")
        #self.k.learn("/home/msunardi/standard/std-lizards.aiml")
        #self.k.learn("/home/msunardi/standard/std-login.aiml")
        #self.k.learn("/home/msunardi/standard/std-numbers.aiml")
        self.k.learn("/home/msunardi/standard/std-personality.aiml")
        #self.k.learn("/home/msunardi/standard/std-pickup.aiml")
        #self.k.learn("/home/msunardi/standard/std-politics.aiml")
        self.k.learn("/home/msunardi/standard/std-profile.aiml")
        #self.k.learn("/home/msunardi/standard/std-religion.aiml")
        #self.k.learn("/home/msunardi/standard/std-robot.aiml")
        #self.k.learn("/home/msunardi/standard/std-sales.aiml")
        #self.k.learn("/home/msunardi/standard/std-sextalk.aiml")
        #self.k.learn("/home/msunardi/standard/std-sports.aiml")
        self.k.learn("/home/msunardi/standard/std-srai.aiml")
        #self.k.learn("/home/msunardi/standard/std-suffixes.aiml")
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
        #    time.sleep(1)
        
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

class FaceDetect (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.faces = 0
        self.pattern = re.compile('There (is|are) (\d+) face? detected')
	self.pattern2 = re.compile('^Name: (\D*)')
        self.pattern3 = re.compile('^Closest match is (\D*) confidence?.$')
        self.doRec = True
        
        sys.path.append("/home/msunardi/Python-project/vision_tests")
    
    def run(self):
        print "Start facedetect"
        #(facedetect_in, facedetect_out) = os.popen2("python pyopencv-test5-facedetect.py")
        (facedetect_in, facedetect_out) = os.popen2("python vision_tests/visionModule.py")
        while True:
            
            faces_detected = facedetect_out.readline()
            #print "Vision message: ", faces_detected
            match = self.pattern.match(faces_detected)
            match2 = self.pattern2.match(faces_detected)
            match3 = self.pattern3.match(faces_detected)
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
            sys.stdout.flush()

    def doRecognize(self):
        self.doRec = True
        return self.doRec

    def toggleRecognize(self):
        return not self.doRec

#==================================
#        TEST
#==================================

"""facedetect = FaceDetect()
#facedetect.start()


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

