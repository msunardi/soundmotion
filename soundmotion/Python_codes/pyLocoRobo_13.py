"""==========================================================
CLASS DESCRIPTION:
   This is the main class which:
   - contains the Main function
   - controls the GUI:
       - loads the GUI (Ui_MainWindow class) & contents (e.g. combobox)
       - assign SIGNALS & SLOTS to the GUI components
       - define actions of SLOT functions
   - controls the loading of data:
       - read data from file:
           - motion data
           - music data
           - ALICE data
       - define how the data is processed.  The processing functions are in:
           - MotionSynthesizer
           - khr1Interface
           - Dialogue
           - resampling
           - and "native" to Python: math, numpy, re, glob

Global variables:
    - self.freqBands        (Type: list) For frequency bands
    - self.originalData          (Type: list) For loaded motion data from file
    - self.newData          (Type: list) For processed (interpolated, gain applied, waveshaped) motion data
    - self.tmpData          (Type: list) Temporary holder for motion data
    - self.bandAdjusters    (Type: list) For values of band adjustments
    - self.ms               (Type: MotionSynthesizer) Instance of MotionSynthesizer
    - self.heartrate        (Type: int, Default value: 30) Default heartrate value
    - self.khr1device       (Type: string, Default value: "/dev/ttyUSB0") Default serial output to KHR1 
    - self.emote_parameters (Type: dictionary) For EMOTE parameters
    - self.dialogueInit     (Type: boolean, Default value: True) Default dialogue state (just starting?)
    - self.dialogueContext  (Type: dictionary) Container for dialogue keywords
    - self.motionFilePath   (Type: list) Selected motion signals
    - self.motionSignalPath (Type: list) List of path to all motion .csv files
    - self.currentMotion    (Type: list, Default value: self.motionFilePath[1]) Current loaded motion
    - self.interpTension    (Type: int, Default value: 0) Tension value for interpolation
    - self.interpBias       (Type: int, Default value: 0) Bias value for interpolation
    - self.interpContinuity (Type: int, Default value: 0) Continuity value for interpolation

Methods:
    - setVariables(self)    returns: None---------------------------------Initialize global variables
    - populateMotionBox(self)   returns: None---------------------------------Populate the KHR1 motion combo box (motions on RCB1)
    - populateMusicBox(self)    returns: None---------------------------------Populate the music combo box
    - populateSignalBox(self, population, defaultIndex=None)    returns: None-Populate the KHR1 motion combo box from .csv files
    - weightChange(self, value) returns: None---------------------------------Action when the Weight slider is changed
    - timeChange(self, value)   returns: None---------------------------------Action when the Time slider is changed
    - spaceChange(self, value)  returns: None---------------------------------Action when the Space slider is changed
    - flowChange(self, value)   returns: None---------------------------------Action when the Flow slider is changed
    - applyGainSignalSlot(self, how_many)   returns: None-----------------Assign SIGNALS & SLOTS to the Gain sliders
    - mapGains(self, how_many)          returns: None-----------------??
    - setSliderValue(self, value, index=None)   returns: None-----------------Set Gain sliders positions
    - adjustGain(self, value)   returns: None---------------------------------Action when the Gain sliders are changed
    - resampleData(self)    returns: None---------------------------------Resample the current interpolated data
    - restoreData(self)     returns: None---------------------------------Reset the original interpolated data
    - loadData(self, path)  returns: None---------------------------------Load a motion signal from file
    - updatePlot(self)      returns: None---------------------------------Update the QwtPlot when changes are made to the signal
    - evaluateExp(self)     returns: None---------------------------------Evaluate Waveshaping formula/expression
    - setPointSlider(self, index)   returns: None-------------------------Set Waveshaping 2 slider position
    - pointLineEditChange(self, value)  returns: None-------------------------Update the Waveshaping 2 LineEdit value/text
    - pointChange(self, value)  returns: None---------------------------------Action when Waveshaping 2 is applied to the signal
    - plotWave(self, target, x, y)  returns: None-------------------------Plot the waveshaping function of Waveshaping 2
    - plotExp(self, target, x, y)   returns: None-------------------------Plot the waveshaping function of Waveshaping 1
    - applyWaveshape(self)  returns: None---------------------------------Superpose Waveshaping 1 with motion signal
    - applyWaveshape2(self) returns: None---------------------------------Superpose Waveshaping 2 with motion signal
    - runData(self)     returns: None---------------------------------Move KHR1 using the current (displayed) motion signal
    - runMotion(self)       returns: None---------------------------------Move KHR1 using selected motion from the motion combo box
    - executeAction(self)   returns: None---------------------------------Move KHR1 according to user interaction e.g.: Dance
    - evaluateBasedOnInput(self, input) returns: None-------------------------Move KHR1 according to user interaction
    - talkToRobot(self)     returns: None---------------------------------Send user input to ALICE/AIML and return response
    - updateDialogueContext(self, inputstring)  returns: None-----------------Update the Context variables
    - updateDialogueContextFields(self) returns: None-------------------------Update the Context variable LineEdits (except Action)
    - updateDialogueContextAction(self, inputstring)    returns: None---------Update the Action Context
    - updateHeartbeat(self, rate)   returns: None-------------------------Update Heart rate

==============================================================
LOGS:
4/20/09:
   - loadData() must be called before the SIGNALS & SLOTS of the Waveshaping 2 tool are assigned, for some reason... (this issue was actually addressed prior to 4/20/09... just forgot to log it in)
4/17/09:
   - Adjusting gains only apply to gains appointed by the index of the slider component.  Gains of other indices are not re-calculated
   - Result: Cannot restore original signal by resetting gains to the original default values (1.0).
==============================================================
"""

# --- Imports
import sys, os, signal
from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
from math import *
import numpy
import re
import glob
from new_ui4_9 import Ui_MainWindow
from mosynth16_p import MotionSynthesizer
from KHR1interface4 import khr1Interface
from dialogueModule import Dialogue
import resampling, autosynthesis, threading
#import pymedia_allplayer as mp3

# --- Class Definition
class MyForm(QtGui.QMainWindow):
    ##=== SECTION 1: LOAD/INITIALIZE GUI COMPONENTS (CB1 - CB11)
    ##CB1 --- Code Block (CB) 1: "constructor"(?)
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        ###CB1.1 --- Build the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ###CB1.2 --- Create class variables (e.g. lists, etc.)
        self.setVariables()

###CB1.3 --- Assign SIGNAL & SLOTS 
        ###CB1.3.1 --- Effort Sliders & Waveshaping function.  These 6 assignments are moved to function "applyGainSignalSlot" because the interface has to be reloaded when loading a different motion file (*REMOVED per 4/19 - pyLocoRobo_06.py*)

                
        ###CB1.3.5 --- Assign action to the self.ui.runbutton
        QtCore.QObject.connect(self.ui.runbutton, QtCore.SIGNAL("released()"), self.runData)

        ###CB1.3.6 --- Assign action to the Toolbar Run button
        QtCore.QObject.connect(self.ui.run, QtCore.SIGNAL("triggered()"), self.runData)

        ###CB1.3.7 --- Assign action to the Toolbar Exit button
        self.connect(self.ui.exit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))

        ###CB1.3.8 --- Assign action to Clear Dialogue button
        QtCore.QObject.connect(self.ui.pushButtonDialogueClear, QtCore.SIGNAL("clicked()"), self.ui.lineEditUserDialogue, QtCore.SLOT("clear()"))

        ###CB1.3.9 --- Assign action to OK Dialogue button
        QtCore.QObject.connect(self.ui.pushButtonDialogueOK, QtCore.SIGNAL("clicked()"), self.talkToRobot)

        ###CB1.3.10 --- Assign action to User Input Field/Line
        QtCore.QObject.connect(self.ui.lineEditUserDialogue, QtCore.SIGNAL("returnPressed()"), self.talkToRobot)

        ###CB1.3.11 --- Assign action to Execute selected motion
        QtCore.QObject.connect(self.ui.pushButtonMotion, QtCore.SIGNAL("clicked()"), self.runMotion)

        QtCore.QObject.connect(self.ui.pushButtonLoadMotion, QtCore.SIGNAL("clicked()"), self.loadMotion)

        ###CB1.4 --- Load song list from folder
        self.songs = glob.glob("/home/msunardi/Music/*.mp3")
                   
        ###CB1.5 --- Load the motion data
        #self.loadData(self.currentMotion)

        ###CB1.6 --- Try to load the Dialogue module
        #### The Dialogue module may sometime not able to load because of competing soundcard usage by other OS components.  Still need to figure this one out.
        try:
            self.dialogue = Dialogue()
        except:
            print "No dialogue this time..."

        ###CB1.7 --- Populate the Motion List combobox (KHR1 memory)
        self.populateMotionBox()

        ###CB1.8 --- Populate the Music/Song List combobox
        self.populateMusicBox()

        ###CB1.9 --- Populate the Motion Signal combobox
        #self.populateSignalBox(self.motionFilePath)
        self.populateSignalBox(self.motionSignalPath)
        self.loadData(self.ui.comboBoxMotionSignal.currentText())  # <<< Load the first motion data to plot

        """=== NOTE (4/16/09):
        For some reason, the data must be populated first, then apply the SIGNAL-SLOT assignments for the Waveshaping2 functions afterwards for them to work.
        ======="""
###CB1.3.2 --- Assign action to Waveshaping2 combobox
        QtCore.QObject.connect(self.ui.pointSelector, QtCore.SIGNAL("currentIndexChanged(int)"), self.setPointSlider)

        ###CB1.3.3a --- Assign action to Waveshaping2 sliderbar: change point value
        QtCore.QObject.connect(self.ui.pointSlider, QtCore.SIGNAL("valueChanged(int)"), self.pointChange)

        ###CB1.3.3b --- Assign action to Waveshaping2 sliderbar: change the value showing in the lineedit
        QtCore.QObject.connect(self.ui.pointSlider, QtCore.SIGNAL("valueChanged(int)"), self.pointLineEditChange)

        ###CB1.3.4 --- Assign action to Waveshaping2 button: apply waveshape to motion signal
        QtCore.QObject.connect(self.ui.pointButton, QtCore.SIGNAL("clicked()"), self.applyWaveshape2)

        ###CB1.10 --- Set up the timer for HeartBeat simulator
        self.timer = QtCore.QBasicTimer()    # <<< CREATE QBasicTimer object
        self.timer.start(self.heartrate, self.ui.ecg)           # <<< START QBasicTimer(interval (ms), QObject)
        self.tryData(self.motionFilePath)

    ##CB2 --- create class' global variables
    def setVariables(self):
        self.freqBands = []   # <<< For frequency bands
        self.originalData = []     # <<< For loaded motion data
        self.newData = []     # <<< For processed motion data
        self.bandAdjusters = []  # <<< For values of band adjustments
        self.ms = MotionSynthesizer()  # <<< Create instance of MotionSynthesizer
        self.heartrate = 30   # <<< Default heartrate value
        self.khr1device = "/dev/ttyUSB0"  # <<< Default serial output to KHR1
        self.emote_parameters = {"weight": 0,"time": 0,"space": 0,"flow": 0}  # <<< For EMOTE parameters
        self.dialogueInit = True  # <<< Default dialogue state (just starting?)
        self.dialogueContext = {"action": "", "topic": "", "username": "", "botname": "", "it": "", "usermood": "", "personality": "", "robotmood": ""}  # <<< Container for dialogue keywords
        self.motionFilePath = ["/home/msunardi/Documents/thesis-stuff/KHR-1-motions/better_fwd_walk_data.csv", 
                                "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv",
                                "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_bird.csv",
                                "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_left.csv",
                                "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv",
                                "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backflip.csv",
                                "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backward_roll.csv",
                                "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH1.csv"]  # <<< Selected motion signals
        self.motionSignalPath = glob.glob("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/*.csv")   # <<< List of all motion files
        self.currentMotion = self.motionFilePath[1]  # <<< Default motion to load: push_ups_data.csv
        self.interpTension = 0
        self.interpBias = 0
        self.interpContinuity = 0
        #self.functions = [interpolate, resampleData2, setSliderValue] 
        self.fparam = {'motion': [], 'interp': {'bias': 0, 'tension': 0, 'continuity': 0}, 'rate': 1, 'gains': {'l':0, 'm':0, 'h':0}, 'waveshapef': '', 'waveshapeg': [], 'awareness': {'orientation':"", 'position':"", 'target':""}}

    ##CB3 --- Populate the motion list combobox (from KHR1 memory)
    def populateMotionBox(self):
        molist = []        
        for i in range(40):
            molist.append(str(i))
        self.ui.comboBoxMotion.addItems(molist)

    ##CB4 --- Populate the music/song list comobobox
    def populateMusicBox(self):
        self.ui.comboBoxMusic.addItems(self.songs)
        self.ui.comboBoxMusic.setCurrentIndex(0)

    ##CB5 --- Populate the selected motion list combobox        
    def populateSignalBox(self, population, defaultIndex=None):
        self.ui.comboBoxMotionSignal.addItems(population)
        if defaultIndex is None:
           self.ui.comboBoxMotionSignal.setCurrentIndex(1)
           #self.ui.comboBoxMotionSignal.setCurrentIndex(4)
        else:
            self.ui.comboBoxMotionSignal.setCurrentIndex(defaultIndex)

    ##CB6 --- SLOT if the Emote Weight slider is changed
    def weightChange(self, value):
        self.ui.weightLineEdit.setText(str(value))
        self.emote_parameters["weight"] = value
        self.ui.statusbar.showMessage("Weight value changed to "+ str(self.emote_parameters["weight"]))        
        #self.ui.qwtPlot.changeCurve(0, range(0, 2*self.emote_parameters["weight"], 1))
        length = len(self.ui.gainSliders)
        index = int(len(self.ui.gainSliders)/2)
        print "index = ", index
        self.ui.gainSliders[index].setSliderPosition(self.ui.gainSliders[index].value() - value)
        self.ui.gainSliders[length-1].setSliderPosition(self.ui.gainSliders[length-1].value() + int(value*0.7))

    ##CB7 --- SLOT if the Emote Time slider is changed
    def timeChange(self, value):
        self.ui.timeLineEdit.setText(str(value))
        self.emote_parameters["time"] = value
        self.ui.statusbar.showMessage("Time value changed to "+ str(self.emote_parameters["time"]))
        
        #self.ui.qwtPlot.changeCurve(1, range(0, 2*self.emote_parameters["weight"], 1))

    ##CB8 --- SLOT if the Emote Space slider is changed
    def spaceChange(self, value):
        self.ui.spaceLineEdit.setText(str(value))
        self.emote_parameters["space"] = value
        self.ui.statusbar.showMessage("Space value changed to "+ str(self.emote_parameters["space"]))

    ##CB9 --- SLOT if the Emote Flow slider is changed
    def flowChange(self, value):
        self.ui.flowLineEdit.setText(str(value))
        self.emote_parameters["flow"] = value
        self.ui.statusbar.showMessage("Flow value changed to "+ str(self.emote_parameters["flow"]))
        self.ui.gainSliders[0].setSliderPosition(self.ui.gainSliders[0].value() - int(value*1.7))

    ##CB10 --- Apply SIGNALS & SLOTS to sliders that directly affects the motion signal
    def applyGainSignalSlot(self, how_many):
        ###CB10.1 --- Create gain sliders depending on the number of frequency components (how_many)
        self.ui.addGainSliders(how_many)

        ###CB10.2 --- These SLOT assignments are down here because the menus had to be refreshed when loading a different motion
        QtCore.QObject.connect(self.ui.weightSlider, QtCore.SIGNAL("valueChanged(int)"), self.weightChange)
        QtCore.QObject.connect(self.ui.timeSlider, QtCore.SIGNAL("valueChanged(int)"), self.timeChange)
        QtCore.QObject.connect(self.ui.spaceSlider, QtCore.SIGNAL("valueChanged(int)"), self.spaceChange)
        QtCore.QObject.connect(self.ui.flowSlider, QtCore.SIGNAL("valueChanged(int)"), self.flowChange)
        QtCore.QObject.connect(self.ui.expEdit, QtCore.SIGNAL("returnPressed()"), self.evaluateExp)
        QtCore.QObject.connect(self.ui.expButton, QtCore.SIGNAL("released()"), self.applyWaveshape)
        QtCore.QObject.connect(self.ui.resamplebutton, QtCore.SIGNAL("released()"), self.resampleData)
        QtCore.QObject.connect(self.ui.restorebutton, QtCore.SIGNAL("released()"), self.restoreData)

        
        ###CB10.3 --- Apply action to each self.ui.gainSliders
        for gs in self.ui.gainSliders:
            
            QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), self.adjustGain)

        for gle in self.ui.gainLineEdits:
            print type(gle)
            QtCore.QObject.connect(gle, QtCore.SIGNAL("returnPressed()"), self.setSliderValue2)

        QtCore.QObject.connect(self.ui.interpTensionSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.setInterpTension)
        QtCore.QObject.connect(self.ui.interpBiasSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.setInterpBias)
        QtCore.QObject.connect(self.ui.interpContinuitySpinBox, QtCore.SIGNAL("valueChanged(int)"), self.setInterpContinuity)
        QtCore.QObject.connect(self.ui.interpButton, QtCore.SIGNAL("clicked()"), self.restoreData)
      
                    
    ##CB11 --- Map gains..?
    def mapGains(self, how_many):
        for i in range(how_many):
            self.bandAdjusters.append(self.adjustGain())
            #print self.bandAdjusters
    
    ##=== END OF SECTION 1

    ##=== SECTION 2: SIGNAL CONTROLS (CB12 - CB25)
    ##CB12 --- Move Gain Slider when position is defined using Gain Lineedits
    def setSliderValue2(self):
        index = int(self.sender().accessibleName())
        self.ui.gainSliders[index].setSliderPosition(int(self.ui.gainLineEdits[index].text())) 
           

    def setSliderValue(self, value, index=None):
        if index is None:
            index = int(self.sender().accessibleName())
       
        self.ui.gainSliders[index].setSliderPosition(int(value))

    ##CB13 --- Apply gain adjustments
    def adjustGain(self, value):
        gainIndex = int(self.sender().accessibleName())

        # === redraw
        self.tmpData = self.ms.DATA
        self.ms.DATA = self.ms.interpolate(self.originalData, self.interpBias, self.interpTension, self.interpContinuity)
        self.ms.multiresFiltering(self.ms.DATA)
        for i in range(self.ms.countGains()):
            for channel in range(self.channels):
                # === if it's not the changed slider...
                if i != gainIndex:
                
                    self.ms.adjustGain(channel, i, self.ui.gainSliders[i].value()*0.1)
                    self.ui.gainLineEdits[i].setText(str(self.ui.gainSliders[i].value()*0.1))
                            
                # === otherwise, it's the changed slider    
                else:

                    self.ms.adjustGain(channel, gainIndex, value*0.1)
                    self.ui.gainLineEdits[gainIndex].setText(str(self.ui.gainSliders[gainIndex].value()*0.1))
                    self.ui.statusbar.showMessage("Band "+self.ui.gainSliders[gainIndex].accessibleName()+" gain changed to "+ str(value*0.1))
                

        self.updatePlot()
        
        print "Sender: %s, value: %f" % (self.sender().accessibleName(), self.sender().value()*0.1)#, self.tmpData[channel]
        self.ms.DATA = self.ms.returnNewData()

    #def adjustGain2(self, motion):                          

    ## --- Interpolate
    def interpolate(self):
        return self.ms.interpolate(self.fparam['motion'], self.fparam['bias'], self.fparam['tension'], self.fparam['continuity'])
  
    ##CB14 --- Resampling
    def resampleData(self):
        resample = resampling.resample
        rate = self.ui.rateSpinBox.value()
        new_data = []
        for data in self.ms.DATA:
            new_data.append(resample(data, rate))
        self.ms.multiresFiltering(new_data)
        self.updatePlot()
        print "sampling..."

    ##CB15 --- Restore original motion signal 
    def restoreData(self):
        tmp = self.ms.interpolate(self.originalData, self.interpBias, self.interpTension, self.interpContinuity)
        self.ms.multiresFiltering(tmp)
        #self.ms.multiresFiltering(self.newData)
        self.updatePlot()

    ##CB16 --- Load and plot selected motion signal data
    def loadData(self, path):
        # === Read data                                   
        self.originalData = self.ms.read(path)

        # === PLOT TITLE
        self.ms.DATA = self.ms.interpolate(self.originalData, self.interpBias, self.interpTension, self.interpContinuity)
        self.freqBands = self.ms.multiresFiltering()
        
        print "Data loaded"

        # === Apply filter
        """ CAUTION!!!  self.originalData is local to this class...
            ... another data already exist within MotionSynthesizer object: self.ms
            ... the internal self.ms data can be accessed as: self.ms.DATA
            All operations on data should be done on the internal (self.ms.DATA)
            This local data (self.originalData) may be used to reset the internal data
        """

        # === global variable # of channels
        self.channels = len(self.ms.DATA)       
        for i in range(self.ms.countGains()):
            for channel in range(self.channels):
                 self.ms.adjustGain(channel, i, 1)

        # === copy the data
        self.newData = self.ms.returnNewData()
        self.tmpData = self.newData     

        self.ui.qwtPlot.reInitialize()
        # === Add curves to plot
        for i in self.newData:
            self.ui.qwtPlot.addCurve(i)
            

        # === Get the bandpass filter bands
        #self.freqBands = self.ms.multiresFiltering(self.newData)
        # === Create sliders for each bands
        self.applyGainSignalSlot(len(self.freqBands[0]))

        self.ui.addBodySpinBoxes(self.newData)

        # === Additional waveshaping data
        self.waveshape = numpy.zeros(len(self.newData))
        self.waveshapePoints = len(self.waveshape)/10 # <<< === careful!!!  if len is < 10..?
        #self.points = numpy.zeros(len(self.originalData[0]))
        #self.new_points = self.ms.interpolate2(self.points)
        indexstring = []
        for i in range(len(self.originalData[0])):
            indexstring.append(str(i))
        print indexstring
        self.ui.pointSelector.addItems(indexstring)
        self.plotWave(self.ui.wavePlot, range(len(self.waveshape)), self.waveshape)

        # --- These are the actual editable points
        self.points = numpy.zeros(len(self.originalData[0]))
        self.new_points = self.ms.interpolate2(self.points)
        self.currentPointIndex = 0

    
    ##CB17 ---
    def updatePlot(self):
        for channel in range(self.channels):
            self.ui.qwtPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))

    def tryData(self, pathlist):
        ml = [self.ms.read(p) for p in pathlist]
        #print "ml=", ml
        print self.concatMotion(ml)

# === WAVESHAPING
    ##CB18 ---
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

# === WAVESHAPING 2
    ##CB19 ---
    def setPointSlider(self, index):
        # Sets the value of the slider with the current index
        
        self.currentPointIndex = index
        point = self.points[index] * 10
        position = int(point)
        self.ui.pointSlider.setSliderPosition(position)  # self.points is in float
        
        print "current point index is: ", self.currentPointIndex

    ##CB20 ---
    def pointLineEditChange(self, value):
        print "point line edit change"
        self.ui.pointLineEdit.setText(str(value * 0.1))

    ##CB21 ---        
    def pointChange(self, value):
        self.points[self.currentPointIndex] = value * 0.1
        print "value in point ", self.currentPointIndex, "= ", self.points[self.currentPointIndex]
        print "points = ", self.points
        self.new_points = self.ms.interpolate2(self.points)
        print "interpolated points: ", self.new_points
        self.plotWave(self.ui.wavePlot, range(len(self.new_points)), self.new_points)

    ##CB22 ---        
    def plotWave(self, target, x, y):   # >>> this is similar to plotExp
        self.waveCurve = Qwt.QwtPlotCurve("waveCurve")
        self.waveCurve.setPen(Qt.QPen(Qt.Qt.red))
        self.waveCurve.setData(x, y)
        self.ui.wavePlot.clear()
        self.waveCurve.attach(target)
        self.ui.wavePlot.replot() 
    
    ##CB23 ---
    def plotExp(self, target, x, y):
        self.expCurve = Qwt.QwtPlotCurve("expCurve")
        self.expCurve.setPen(Qt.QPen(Qt.Qt.blue))
        self.expCurve.setData(x, y)
        self.ui.expPlot.clear()
        self.expCurve.attach(target)
        self.ui.expPlot.replot()

    ##CB24 --- 
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

    ##CB25 --- 
    def applyWaveshape2(self):
        try:
            tmp = []
            data = self.ms.returnNewData()
            print "click"

            for i in range(len(data)):
                try:
                    tmpData = list(numpy.add(data[i], numpy.multiply(data[i], self.new_points)))
                    self.ui.statusbar.showMessage("Applying waveshape 2...")                    
                except:
                    #print "length data: ", len(data[i]), "points = ", len(self.new_points)
                    self.ui.statusbar.showMessage("Waveshape 2 failed.")
                tmp.append(tmpData)
                self.ui.qwtPlot.changeCurve(i, tmpData)

            #self.newData = tmp
            self.ms.DATA = tmp
                
        except:
            self.ui.statusbar.showMessage("Uh oh, something is wrong...")

    #================FUNCTIONS FOR AUTONOMOUS MOTION SYNTHESIS=====================================5/4/09: 7:48pm
    
    def setInterpTension(self, value):
        print "Old Tension =", self.interpTension,
        self.interpTension = value
        self.fparam['interp']['tension'] = value
        print "new Tension =", self.interpTension

    def setInterpBias(self, value):
        print "Old Bias =", self.interpBias,
        self.interpBias = value
        self.fparam['interp']['bias'] = value
        print "new Bias =", self.interpBias

    def setInterpContinuity(self, value): 
        print "Old Continuity =", self.interpContinuity,
        self.interpContinuity = value
        self.fparam['interp']['continuity'] = value
        print "new Continuity =", self.interpContinuity
    
    def loadMotion(self):
        self.loadData(self.ui.comboBoxMotionSignal.currentText())
    
    def setMotion(self, motion):
        self.fparam['motion'].append(motion)

    def clearMotion(self):
        self.fparam['motion'] = []

    def interpolate(self):
        return self.ms.interpolate(self.fparam['motion'], self.fparam['interp']['bias'], self.fparam['interp']['tension'], self.fparam['interp']['continuity'])

    def resampleData2(self):
        resample = resampling.resample
        #rate = self.ui.rateSpinBox.value()
        self.ui.rateSpinBox.setValue(self.fparams['rate'])
        new_data = []
        for data in self.ms.DATA:
            new_data.append(resample(data, rate))
        self.ms.multiresFiltering(new_data)
        self.updatePlot()
        print "autosampling..."

    def modifyGains(self):
        n = len(self.ms.countGains())
        [start, step] = self.defstep(n)
        indices = range(start, n, step)
        for i in range(0,3):
            self.setSliderValue(self.fparam['gains'][i], indices[i])
        
    def defstep(self, x):
         # given x number of gains, find the low, medium, high gain indices
         # returns: initial index, steps
         s = x%3
         f = x/3
         if s > 1:
             return f-1, f+1
         else:
             return f-1, f
    
    #def concatMotion(self):
    def concatMotion(self, motionlist):
        if len(self.fparam['motion']) < 2:
            print "Need 2 or more motions to concatenate."
            return 0
        else:
            return reduce(lambda m1, m2: self.ms.concatenatemotion(m1,m2), motionlist)

    def concatMotion2(self):
        pass

    def superpose(self, motion1, motion2):
        try:
            tmp = []
            #data = self.ms.returnNewData()
            print "Superpose!"

            for i in range(len(motion1)):
                try:
                    tmpData = list(numpy.add(motion1[i], numpy.multiply(motion2[i], 0.5)))
                    self.ui.statusbar.showMessage("Superposing...")                    
                except:
                    #print "length data: ", len(data[i]), "points = ", len(self.new_points)
                    self.ui.statusbar.showMessage("Waveshape 2 failed.")
                tmp.append(tmpData)
                self.ui.qwtPlot.changeCurve(i, tmpData)

            #self.newData = tmp
            self.ms.DATA = tmp
                
        except:
            self.ui.statusbar.showMessage("Uh oh, something is wrong...")

    def evaluateExp2(self):
        try:
            text = unicode(self.fparam['waveshapef'])
            #x = 2
            self.ui.statusbar.showMessage("Auto-Waveshaping function(x) = %s" % (text))
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
        self.applyWaveshapef()

    def applyWaveshapef(self):
        multiplier = 0.15
        try:
            tmp = []
            data = self.ms.returnNewData()

            for i in range(len(data)):
                tmpData = list(numpy.add(data[i], numpy.multiply(data[i], numpy.multiply(self.y, multiplier))))
                tmp.append(tmpData)
                self.ui.qwtPlot.changeCurve(i, tmpData)

            #self.newData = tmp
            self.ms.DATA = tmp
            self.ui.expSpinBox.setValue(multiplier)
                
        except:
            self.ui.statusbar.showMessage("Uh oh, something is wrong...")
    """
    """
    def waveshapeg (self):  # derived from self.pointChange(...)
        try:
            print "Applying waveshapeg"
            
            for p in self.fparam['waveshapeg']:
                self.points[p[0]] = p[1] * 0.1
            #print "value in point ", self.currentPointIndex, "= ", self.points[self.currentPointIndex]
            #print "points = ", self.points
            self.new_points = self.ms.interpolate2(self.points)
            #print "interpolated points: ", self.new_points
            self.plotWave(self.ui.wavePlot, range(len(self.new_points)), self.new_points)
        except:
            print "Waveshapeg failed..."
    """ 
    """
    def plotWave(self, target, x, y):   # >>> this is similar to plotExp
        self.waveCurve = Qwt.QwtPlotCurve("waveCurve")
        self.waveCurve.setPen(Qt.QPen(Qt.Qt.red))
        self.waveCurve.setData(x, y)
        self.ui.wavePlot.clear()
        self.waveCurve.attach(target)
        self.ui.wavePlot.replot()

    def awareness(self):
        pass
    
    #self.ffunct = {'interpolate':self.interpolate, 'resample':self.resampleData2, 'modifygains':self.modifyGains, 'blend':self.concatMotion, 'waveshapefunct': self.waveshapef, 'waveshapegraph': self.waveshapeg}
    #self.ffunctlist = [self.interpolate, self.resampleData2, self.modifyGains, self.waveshapef, self.waveshapeg, self.concatMotion, self.awareness]
    
    
    ##=== END OF SECTION 2

    ##=== SECTION 3: OUTPUT (CB26 - CB34) 
    ##CB26 --- Send motion signal data to Robot
    def runData(self):
        khr1Interface(self.khr1device, self.ms.DATA).start()
        khr1Interface(self.khr1device, "home").start()
    
    ##CB27 --- Run selected motion from KHR1 memory    
    def runMotion(self):
        motion = int(self.ui.comboBoxMotion.currentText())
        khr1Interface("/dev/ttyUSB0", motion).start()
        
        #khr1Interface("/dev/ttyUSB0", "home").start()
 
    ##CB28 --- Executing actions from dialogue
    def executeAction(self):
        if self.dialogueContext["action"] == "dance":
            print "Executing action: ", self.dialogueContext["action"]
            khr1Interface("/dev/ttyUSB0", "dance").start()
            os.system("/etc/init.d/speech-dispatcher stop")
            #os.popen("python pymedia_allplayer.py /home/msunardi/Music/02-4Minutes.mp3")
            #os.popen("python pymedia_allplayer.py /home/msunardi/Music/06-BoogieTonight.mp3")
            music = str(self.ui.comboBoxMusic.currentText())
            playmusic = "python pymedia_allplayer.py " + music
            print playmusic
            
            self.musicPid = os.fork()
            if self.musicPid == 0:  # The child process to play music
                os.popen(playmusic)
                #os.system("/etc/init.d/speech-dispatcher restart")
                exit()
            
            print "Music played\n"
            #os.execvp("/etc/init.d/speech-dispatcher", ["/etc/init.d/speech-dispatcher", "restart"])
            khr1Interface("/dev/ttyUSB0", "home").start()
        if self.dialogueContext["action"] == "greet":
            khr1Interface("/dev/ttyUSB0", 2).start() 
        self.dialogueContext["action"] = ""
        #os.system("/etc/init.d/speech-dispatcher start")
    

    ##CB29 ---
    def evaluateBasedOnInput(self, input):
        try:
            self.ui.statusbar.showMessage("Waveshaping function(x) = sin(0.02*x)")
            c = 0
            self.y = []
            currentData = self.ms.returnNewData()
            for x in range(len(currentData[0])):
                if input == 'abusive':
                    c = sin(0.02*x)
                elif input == 'sad':
                    c = sin(0.02*x + 0.5*pi)
                elif input == 'happy':
                    c = sin(0.2*x + 0.5*pi)
                elif input == 'average':
                    c = 1
                elif not ['abusive', 'sad', 'happy'].__contains__(input):
                    break
                self.y.append(c)
                c = 0
            
            self.ui.statusbar.showMessage("Trying some LMA...")
            if ['heavy', 'light', 'fast', 'slow', 'free', 'bound', 'direct', 'indirect'].__contains__(input):
                for x in range(len(currentData[0])):
                    c = 1
                    self.y.append(c)
                    c = 0
            
            for i in range(len(self.y)):
                self.y[i] = float(self.y[i])/max(self.y)

        except:
            self.ui.statusbar.showMessage("Uh oh...")
        self.plotExp(self.ui.expPlot, range(len(currentData[0])), self.y)

    ##CB30 ---
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
            if not self.dialogueContext["personality"] == '':
                self.evaluateBasedOnInput(self.dialogueContext["personality"])
        threading.Thread(target=self.jello(getUserInput)).start()

        self.dialogueInit = False
       
        self.ui.lineEditUserDialogue.clear()
        try:
            self.ui.statusbar.showMessage("I see "+self.dialogue.facedetect.faces+" face(s)")
        except:
            self.ui.statusbar.showMessage("I can't see anything...")
    
    ##CB31 ---
    def updateDialogueContext(self, inputstring):
        self.ui.lineEditAction.setText(self.dialogue.getValues("GET ACTION"))
        self.dialogueContext["topic"] = self.dialogue.getValues("GET TOPIC")
        self.dialogueContext["username"] = self.dialogue.getValues("GET USERNAME")
        self.dialogueContext["usermood"] = self.dialogue.getValues("GET USERMOOD")
        self.dialogueContext["it"] = self.dialogue.getValues("GET IT")
        self.dialogueContext["personality"] = self.dialogue.getValues("GET PERSONALITY")
        self.dialogueContext["robotmood"] = self.dialogue.getValues("GET ROBOTMOOD")
        self.dialogue.getValues(inputstring)

    ##CB32 --- 
    def updateDialogueContextFields(self):
        self.ui.lineEditTopic.setText(self.dialogueContext["topic"])
        self.ui.lineEditIt.setText(self.dialogueContext["it"])
        self.ui.lineEditUsername.setText(self.dialogueContext["username"])
        self.ui.lineEditUsermood.setText(self.dialogueContext["usermood"])
        self.ui.lineEditPersonality.setText(self.dialogueContext["personality"])
        self.ui.lineEditRobotmood.setText(self.dialogueContext["robotmood"])
        #self.ui.lineEditAction.setText(self.dialogueContext["action"])
        #if not self.dialogueContext["action"] == "":
        #    self.executeAction()

    ##CB33 ---
    def updateDialogueContextAction(self, inputstring):
        print inputstring

        self.keywords = []
        self.motions = []
        self.pattern = re.compile('i\'ll (dance|greet).$', re.I)
        self.pattern2 = re.compile('^hello', re.I)
        self.pattern3 = re.compile('bye', re.I)
        match = self.pattern.match(inputstring)
        match2 = self.pattern2.match(inputstring)
        match3 = self.pattern3.match(inputstring)
        inputstring = inputstring.lower()
        print "inputstring: ", inputstring  
        if inputstring.__contains__('i\'ll dance'):
            #print type(match.group(1))
            self.dialogueContext["action"] = "dance"
            self.ui.lineEditAction.setText("dance")
            self.executeAction()
        elif inputstring.__contains__('hello') or inputstring.__contains__('bye'):
            self.dialogueContext["action"] = "greet"
            self.ui.lineEditAction.setText("greet")
            self.updateHeartbeat(10)
            self.executeAction()
        elif inputstring.__contains__('calm'):
            self.updateHeartbeat(self.heartrate)
        elif inputstring.__contains__('tired'):
            self.ui.statusbar.showMessage("Robot is tired.")
            self.updateHeartbeat(self.heartrate-10)
            self.setSliderValue(-2, 2)
        elif inputstring == 'word!':
            try:
                print "killing musicpid:", self.musicPid
                os.kill(self.musicPid, signal.SIGKILL)
                os.kill(self.musicPid+2, signal.SIGKILL)
            except:
                print "Music is already off."
            os.system("/etc/init.d/speech-dispatcher restart")
            print "Stopped music, restoring speech..."
        else:
            self.dialogueContext["action"] = ""
            self.ui.lineEditAction.setText("")

    
    ##CB34 ---
    def updateHeartbeat(self, rate):
        print "heart"
        self.timer.stop()
        self.timer.start(rate, self.ui.ecg)

    def jello(self, inputstring):
        #interp: bias,tension,continuity
        #sampling: rate
        #gains: lgains, mgains, hgains
        #waveshape: function, index, value
        #blend: [motions]
        #awareness: position/direction
        
        print "jello"
        pat1 = re.compile('exit[()]')
        pat2 = re.compile('\d+')
        pat3 = re.compile('\w*\s*(fall)+\w*')
        pat4 = re.compile('(^|\w*\s+)+(I)+\s+\w*')
        pat5 = re.compile('(^|\s*\w*|\w*\s*|\W*)*(i(\s+am|\'m)+ (mad|angry|happy|sad|afraid|worried|tired|bored)+)+\w*', re.IGNORECASE)
        #pat6 = re.compile('(^|\w*\s*)+(relax|laugh|cry|talk|walk|run|jump|hit|bow|pick|lick)+\w*')

        #m1 = pat2.match(inputstring)
        #m2 = pat3.match(inputstring)
        #m3 = pat4.match(inputstring)
        m4 = pat5.match(inputstring)
        #m5 = pat6.match(inputstring)

        if m4:
            f = pat5.findall(inputstring)
            if f[0][3] == 'mad':
                self.sampling = 3
                self.mgains = 2
            elif f[0][3] == 'angry':
                self.sampling = 3
            print m4.groups()
                

    """def applyContext(self, paramvalues=self.signalParams):
        interp = paramvalues['interp']  #list: [bias, tension, continuity]
        rate = paramvalues['sampling']  #int: rate
        gains = paramvalues['gains']    #list: [hgain, mgain, lgain]
        waveshape = paramvalues['waveshape']    #funct: wvfunct
        wavashape2 = paramvalues['waveshape2']  #list: [[index, value], ...]
        mblend = paramvalues['mblend']  #list: [motion1, motion2, ...]"""
        
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
