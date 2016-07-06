import sys, os
from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
from math import *
import numpy
import re
from new_ui4_6 import Ui_MainWindow
from mosynth10_p import MotionSynthesizer
from KHR1interface3 import khr1Interface
from dialogueModule import Dialogue
#import pymedia_allplayer as mp3

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.emote_parameters = {"weight": 0, "time": 0, "space": 0, "flow": 0}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setVariables()
        #QtCore.QObject.connect(self.ui.weightSlider, QtCore.SIGNAL("valueChanged(int)"), self.weightChange)
        #QtCore.QObject.connect(self.ui.timeSlider, QtCore.SIGNAL("valueChanged(int)"), self.timeChange)
        #QtCore.QObject.connect(self.ui.spaceSlider, QtCore.SIGNAL("valueChanged(int)"), self.spaceChange)
        #QtCore.QObject.connect(self.ui.flowSlider, QtCore.SIGNAL("valueChanged(int)"), self.flowChange)
        #QtCore.QObject.connect(self.ui.expEdit, QtCore.SIGNAL("returnPressed()"), self.evaluateExp)
        #QtCore.QObject.connect(self.ui.expButton, QtCore.SIGNAL("released()"), self.applyWaveshape)
        # === Apply action to the self.ui.runbutton
        QtCore.QObject.connect(self.ui.runbutton, QtCore.SIGNAL("released()"), self.runData)
        QtCore.QObject.connect(self.ui.run, QtCore.SIGNAL("triggered()"), self.runData)
        self.connect(self.ui.exit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))
        QtCore.QObject.connect(self.ui.pushButtonDialogueClear, QtCore.SIGNAL("clicked()"), self.ui.lineEditUserDialogue, QtCore.SLOT("clear()"))
        QtCore.QObject.connect(self.ui.pushButtonDialogueOK, QtCore.SIGNAL("clicked()"), self.talkToRobot)
        QtCore.QObject.connect(self.ui.lineEditUserDialogue, QtCore.SIGNAL("returnPressed()"), self.talkToRobot)
        QtCore.QObject.connect(self.ui.pushButtonMotion, QtCore.SIGNAL("clicked()"), self.runMotion)

        self.loadData()

        self.dialogue = Dialogue()
        self.dialogueInit = True
        self.dialogueContext = {"action": "", "topic": "", "username": "", "botname": "", "it": "", "usermood": "", "personality": ""}

        self.populateMotionBox()

        #self.x = QtGui.QTextEdit(self.ui)

        #test:
        #self.ui.qwtPlot.addCurve(range(0,200,1))
        #self.ui.qwtPlot.addCurve(range(0,200,1))
        #works!

    def setVariables(self):
        self.freqBands = []
        self.allData = []
        self.newData = []
        self.bandAdjusters = []
        self.ms = MotionSynthesizer()
        #self.khr1 = khr1Interface("/dev/ttyUSB0")

    def populateMotionBox(self):
        list = []        
        for i in range(40):
            list.append(str(i))
        self.ui.comboBoxMotion.addItems(list)
        

    def weightChange(self,  value):
        self.ui.weightLineEdit.setText(str(value))
        self.emote_parameters["weight"] = value
        self.ui.statusbar.showMessage("Weight value changed to "+ str(self.emote_parameters["weight"]))        
        #self.ui.qwtPlot.changeCurve(0, range(0, 2*self.emote_parameters["weight"], 1))
        length = len(self.ui.gainSliders)
        index = int(len(self.ui.gainSliders)/2)
        print "index = ", index
        self.ui.gainSliders[index].setSliderPosition(self.ui.gainSliders[index].value() - value)
        self.ui.gainSliders[length-1].setSliderPosition(self.ui.gainSliders[length-1].value() + int(value*0.7))

    def timeChange(self, value):
        self.ui.timeLineEdit.setText(str(value))
        self.emote_parameters["time"] = value
        self.ui.statusbar.showMessage("Time value changed to "+ str(self.emote_parameters["time"]))
        
        #self.ui.qwtPlot.changeCurve(1, range(0, 2*self.emote_parameters["weight"], 1))

    def spaceChange(self, value):
        self.ui.spaceLineEdit.setText(str(value))
        self.emote_parameters["space"] = value
        self.ui.statusbar.showMessage("Space value changed to "+ str(self.emote_parameters["space"]))
        #self.ui.addGainSliders(self.emote_parameters["weight"])
        #print type(self.ui.gainSliders[0])

    def flowChange(self, value):
        self.ui.flowLineEdit.setText(str(value))
        self.emote_parameters["flow"] = value
        self.ui.statusbar.showMessage("Flow value changed to "+ str(self.emote_parameters["flow"]))
        self.ui.gainSliders[0].setSliderPosition(self.ui.gainSliders[0].value() - int(value*1.7))

    def applyGainSignalSlot(self, how_many):
        self.ui.addGainSliders(how_many)
        QtCore.QObject.connect(self.ui.weightSlider, QtCore.SIGNAL("valueChanged(int)"), self.weightChange)
        QtCore.QObject.connect(self.ui.timeSlider, QtCore.SIGNAL("valueChanged(int)"), self.timeChange)
        QtCore.QObject.connect(self.ui.spaceSlider, QtCore.SIGNAL("valueChanged(int)"), self.spaceChange)
        QtCore.QObject.connect(self.ui.flowSlider, QtCore.SIGNAL("valueChanged(int)"), self.flowChange)
        QtCore.QObject.connect(self.ui.expEdit, QtCore.SIGNAL("returnPressed()"), self.evaluateExp)
        QtCore.QObject.connect(self.ui.expButton, QtCore.SIGNAL("released()"), self.applyWaveshape)

        print "gain sliders: "+str(how_many)
        

        # === Apply action to each self.ui.gainSliders
        for gs in self.ui.gainSliders:
            
            QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), self.adjustGain)

        for gle in self.ui.gainLineEdits:

            #QtCore.QObject.connect(gle, QtCore.SIGNAL("valueChanged(double)"), self.setSliderValue) # use new_ui3_copy3 for this
            QtCore.QObject.connect(gle, QtCore.SIGNAL("returnPressed()"), self.setSliderValue)
                    


    def mapGains(self, how_many):
        for i in range(how_many):
            self.bandAdjusters.append(self.adjustGain())
            #print self.bandAdjusters

#====== SIGNAL SECTION
    def setSliderValue(self, value):
        index = int(self.sender().accessibleName())
        #self.ui.gainSliders[index].setSliderPosition(int(value))
        self.ui.gainSliders[index].setSliderPosition(int(value))
            
    def adjustGain(self, value):
        """new = self.ms.mrfDoItAll(self.newData, 0, 0, self.ui.gainSliders[0].value)
        for i in range(len(new)):
            self.ui.qwtPlot.changeCurve(i, new[i])
        self.ui.qwtPlot.plotCurves()        
        """
        # self.sender() -- hidden method, to identify which object just sent a signal
        #print self.sender().accessibleName()

        #channel = 7
        gainIndex = int(self.sender().accessibleName())
        #mx = self.ms.mrfDoItAll(self.newData, channel, self.ms.countGains(), self.ui.gainSliders[1].value()*0.1)
        #mx = self.ms.mrfDoItAll(self.newData, channel, self.ms.countGains(), value*0.1)
        #print "channels: "+str(len(self.newDat

        # === modify the gains for the corresponding bands for all channels
        #for channel in range(self.channels)):
            #self.tmpData = self.ms.mrfDoItAll(self.newData, channel, gainIndex, value)
        #self.tmpData = self.newData
        # === redraw
        self.tmpData = self.ms.DATA
        self.ms.DATA = self.ms.interpolate(self.allData)
        self.ms.multiresFiltering(self.ms.DATA)
        #print self.ms.DATA[0]
        for i in range(self.ms.countGains()):
            #print "countGains range: ", self.ms.countGains()
            for channel in range(self.channels):
                # === if it's not the changed slider...
                if i != gainIndex:
                
                    #self.tmpData = self.ms.mrfDoItAll(self.tmpData, channel, i, self.ui.gainSliders[i].value())\
                    self.ms.adjustGain(channel, i, self.ui.gainSliders[i].value()*0.1)
                    self.ui.gainLineEdits[i].setText(str(self.ui.gainSliders[i].value()*0.1))
                    #self.ui.gainLineEdits[i].setValue(self.ui.gainSliders[i].value()*0.1) # use new_ui3_copy3 for this
                            
                # === otherwise, it's the changed slider    
                else:
                    #self.tmpData = self.ms.mrfDoItAll(self.tmpData, channel, gainIndex, value)
                    self.ms.adjustGain(channel, gainIndex, value*0.1)
                    self.ui.gainLineEdits[gainIndex].setText(str(self.ui.gainSliders[gainIndex].value()*0.1))
                    #self.ui.gainLineEdits[gainIndex].setValue(self.ui.gainSliders[gainIndex].value()*0.1) # use new_ui3_copy3 for this
                    self.ui.statusbar.showMessage("Band "+self.ui.gainSliders[gainIndex].accessibleName()+" gain changed to "+ str(value*0.1))

                # === 
                #self.ui.qwtPlot.changeCurve(channel, self.tmpData[channel])
                #self.ui.qwtPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))

        for channel in range(self.channels):
            self.ui.qwtPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))
        
        print "Sender: %s, value: %f" % (self.sender().accessibleName(), self.sender().value()*0.1)#, self.tmpData[channel]
        #print "number of gains", type(self.ms.countGains())
        self.ms.DATA = self.ms.returnNewData()

        #self.ui.qwtPlot.changeCurve(channel, self.tmpData[])
        #pass
   
    def runData(self):
        khr1Interface("/dev/ttyUSB0", self.ms.DATA).start()
        #self.khr1.run(self.ms.returnNewData())
        #self.khr1.run(self.ms.returnNormalized())        
        khr1Interface("/dev/ttyUSB0", "home").start()

        
    def runMotion(self):
        motion = int(self.ui.comboBoxMotion.currentText())
        khr1Interface("/dev/ttyUSB0", motion).start()
        
        khr1Interface("/dev/ttyUSB0", "home").start()
 
    #--- Executing actions
    def executeAction(self):
        if self.dialogueContext["action"] == "dance":
            print "Executing action: ", self.dialogueContext["action"]
            khr1Interface("/dev/ttyUSB0", "dance").start()
            os.system("/etc/init.d/speech-dispatcher stop")
            #os.popen("python pymedia_allplayer.py /home/msunardi/Music/02-4Minutes.mp3")           
            os.popen("python pymedia_allplayer.py /home/msunardi/Music/06-BoogieTonight.mp3")           

            #os.wait()
            os.system("/etc/init.d/speech-dispatcher start")
            khr1Interface("/dev/ttyUSB0", "home").start()
        if self.dialogueContext["action"] == "greet":
            khr1Interface("/dev/ttyUSB0", 2).start() 
        self.dialogueContext["action"] = ""
        #khr1Interface("/dev/ttyUSB0", "home").start()
        os.system("/etc/init.d/speech-dispatcher start")


    def loadData(self):
        # === Read data                                   
        #self.allData = self.ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/better_fwd_walk_data.csv")
        self.allData = self.ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
        self.ui.qwtPlot.setTitle("push_ups_data.csv")
        #self.ms.DATA = self.allData
        self.ms.DATA = self.ms.interpolate(self.allData)
        self.ms.multiresFiltering()
        
        print "Data loaded"

        # === Apply filter
        """ CAUTION!!!  self.allData is local to this class...
            ... another data already exist within MotionSynthesizer object: self.ms
            ... the internal self.ms data can be accessed as: self.ms.DATA
            All operations on data should be done on the internal (self.ms.DATA)
            This local data (self.allData) may be used to reset the internal data
        """
        tmp = self.ms.mrfDoItAll(self.allData)
        #tmp = self.ms.interpolate(self.allData)
        # === Apply interpolation
        self.newData = self.ms.interpolate(tmp)
        #self.newData = self.ms.mrfDoItAll(tmp)
        #self.newData = self.ms.interpolate(self.allData)

        # === global variable # of channels
        self.channels = len(self.newData)
        
        for i in range(self.ms.countGains()):
            for channel in range(self.channels):
                 self.ms.adjustGain(channel, i, 1)

        # === copy the data
        self.newData = self.ms.returnNewData()
        self.tmpData = self.newData     

        
        # === Add curves to plot
        for i in self.newData:
        #for i in self.ms.DATA:
            self.ui.qwtPlot.addCurve(i)
            
        #self.ui.qwtPlot.addCurve(self.newData[0])

        # === Get the bandpass filter bands
        self.freqBands = self.ms.multiresFiltering(self.newData)
        # === Create sliders for each bands
        self.applyGainSignalSlot(len(self.freqBands[0]))
        print self.freqBands[0]

        self.ui.addBodySpinBoxes(self.newData)
        print len(self.newData)
        print len(self.newData[0])

        #self.ms.DATA = self.newData

    def evaluateExp(self):
        try:
            text = unicode(self.ui.expEdit.text())
            #x = 2
            self.ui.statusbar.showMessage("Waveshaping function(x) = %s" % (text))
            c = 0
            self.y = []

            currentData = self.ms.returnNewData()
            for x in range(len(currentData[0])):
                c = eval(text)
                self.y.append(c)                
                c = 0            

            #print "y: ", y

            # == Normalize
            for i in range(len(self.y)):
                self.y[i] = float(self.y[i])/max(self.y)

            #print "new y: ",y
            
        except:
            self.ui.statusbar.showMessage("%s is invalid!" % text)

        self.plotExp(self.ui.expPlot, range(len(currentData[0])), self.y)


    def plotExp(self, target, x, y):
        self.expCurve = Qwt.QwtPlotCurve("expCurve")
        self.expCurve.setPen(Qt.QPen(Qt.Qt.blue))
        self.expCurve.setData(x, y)
        self.ui.expPlot.clear()
        self.expCurve.attach(target)
        self.ui.expPlot.replot()

    def applyWaveshape(self):
        try:
            tmp = []
            data = self.ms.returnNewData()

            for i in range(len(data)):
                tmpData = list(numpy.add(data[i], numpy.multiply(data[i], numpy.multiply(self.y, self.ui.expSpinBox.value()))))
                tmp.append(tmpData)
                self.ui.qwtPlot.changeCurve(i, tmpData)

            #self.newData = tmp
            self.ms.DATA = tmp
                
        except:
            self.ui.statusbar.showMessage("Uh oh, something is wrong...")
  
   
    def talkToRobot(self):
        getUserInput = self.ui.lineEditUserDialogue.text()
        #print "Input: ", getUserInput, "type: ", type(str(getUserInput))
        getUserInput = str(getUserInput)
        response = self.dialogue.youSay(getUserInput)
        self.ui.textBrowserRobotResponse.append("> %s" % (str(getUserInput)))
        self.ui.textBrowserRobotResponse.append("<b><font color=blue>%s</font></b>" % (response))
        if not self.dialogueInit:
            self.updateDialogueContext(str(getUserInput))
            self.updateDialogueContextFields()
            if self.ui.lineEditAction.text() != '':
                self.updateDialogueContextAction(response)

        self.dialogueInit = False
       
        self.ui.lineEditUserDialogue.clear()
        self.ui.statusbar.showMessage("I see "+self.dialogue.facedetect.faces+" face(s)")
    
    def updateDialogueContext(self, inputstring):
        #self.dialogueContext["action"] = self.dialogue.getValues("GET ACTION")
        self.ui.lineEditAction.setText(self.dialogue.getValues("GET ACTION"))
        self.dialogueContext["topic"] = self.dialogue.getValues("GET TOPIC")
        self.dialogueContext["username"] = self.dialogue.getValues("GET USERNAME")
        self.dialogueContext["usermood"] = self.dialogue.getValues("GET USERMOOD")
        self.dialogueContext["it"] = self.dialogue.getValues("GET IT")
        self.dialogueContext["personality"] = self.dialogue.getValues("GET PERSONALITY")
        self.dialogue.getValues(inputstring)

    def updateDialogueContextFields(self):
        self.ui.lineEditTopic.setText(self.dialogueContext["topic"])
        self.ui.lineEditIt.setText(self.dialogueContext["it"])
        self.ui.lineEditUsername.setText(self.dialogueContext["username"])
        self.ui.lineEditUsermood.setText(self.dialogueContext["usermood"])
        self.ui.lineEditPersonality.setText(self.dialogueContext["personality"])
        #self.ui.lineEditAction.setText(self.dialogueContext["action"])
        #if not self.dialogueContext["action"] == "":
        #    self.executeAction()

    def updateDialogueContextAction(self, inputstring):
        print inputstring
        self.pattern = re.compile('i\'ll (dance|greet).$', re.I)
        self.pattern2 = re.compile('^hello', re.I)
        self.pattern3 = re.compile('bye', re.I)
        match = self.pattern.match(inputstring)
        match2 = self.pattern2.match(inputstring)
        match3 = self.pattern3.match(inputstring)
        if inputstring.__contains__('I\'ll dance'):
            #print type(match.group(1))
            self.dialogueContext["action"] = "dance"
            self.ui.lineEditAction.setText("dance")
            self.executeAction()
        elif inputstring.__contains__('hello') or inputstring.__contains__('bye'):
            self.dialogueContext["action"] = "greet"
            self.ui.lineEditAction.setText("greet")
            self.executeAction()
        else:
            self.dialogueContext["action"] = ""
            self.ui.lineEditAction.setText('')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
