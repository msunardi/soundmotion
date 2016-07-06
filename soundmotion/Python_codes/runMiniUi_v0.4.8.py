import sys, glob, re, resampling

import PyQt4.Qwt5 as Qwt
from PyQt4 import QtCore, QtGui, Qt
from pyMiniUix_v8 import Ui_MainWindow
from mosynth20_p import MotionSynthesizer
from locoKHR1Interface_v8 import khr1Interface
#from KHR1interface8 import khr1Interface
from dialogueModule import Dialogue
from LocoContext14 import locoContext
from scriptReadCsv import readScript

class MyForm(QtGui.QMainWindow):
		
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.setVariables()
		
		self.ui.populateChannelList()
		self.setActions()
		self.motionPath = self.loadMotionFiles()
		
		self.formatMotionList(self.motionPath)
		
		self.ui.populateKhr1MotionBox()
		
		#self.ui.populateMotionBox(self.formatMotionList(self.motionSignalPath))		
		self.ui.populateMotionBox([k for k,v in self.motionSignalPath.items()])
		#self.loadData(self.motionSignalPath[self.ui.motionComboBox.currentIndex()])
		print self.ui.motionComboBox.currentText()
		#self.loadData(self.motionSignalPath[self.ui.motionComboBox.currentText()])
		self.loadData(dataIndex=self.ui.motionComboBox.currentText())
		
	def setVariables(self):
		# Containers...
		self.motionPath = []	# list of path to .csv files loaded using glob
		self.motionSignalPath = {}	# dictionary of path to .csv files indexed by file name		
		self.CURRENT_MOTION_DATA = []	# container for current loaded motion data from file
		self.CURRENT_INTERP_MOTION_DATA = []	# container for current interpolated motion data
		self.OUTPUT_DATA = []
		self.SCRIPT = []
		self.chatoptions = {}
		
		# Parameters...
		self.interpParameters = {'tension': 0, 'bias': 0, 'continuity': 0}	# interpolation parameters
		self.affectProcessing = False
		self.dialogueInit = True
		
		# Constants...
		self.defaultMotionPath = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/"
		self.khr1Device = "/dev/ttyUSB0"
		scriptpath = 'scripts/script1.csv'
		
		# Class instances...
		self.ms = MotionSynthesizer()
		try:
			self.dialogue = Dialogue()			
		except:
			print "No dialogue this time..."

		try:
			self.lcontext = locoContext()
		except:
			print "No lococontext this time..."
			
		try:
			rs = readScript()
			self.SCRIPT = rs.read(scriptpath)
			print "Script: %s is loaded." % scriptpath
			self.scriptindex=0
		except:
			print "Failed loading Script."
		
	def setActions(self):
		print "setActions"
		
		self.setActionsChannelsCheckBox()
		self.setActionsAffectProcessingCheckBox()		
		self.setActionsMotionControls()
		self.setActionsMotionFile()
		
		self.setTabActions()
		self.setToolbarActions()
		self.setActionsRobotState()
		self.setActionsChatUI()		
		
	def setActionsChatUI(self):
		QtCore.QObject.connect(self.ui.chatInputClearButton, QtCore.SIGNAL("clicked()"), self.ui.chatInput, QtCore.SLOT("clear()"))
		QtCore.QObject.connect(self.ui.chatInputEnterButton, QtCore.SIGNAL("clicked()"), self.talkToRobot)
		QtCore.QObject.connect(self.ui.chatInput, QtCore.SIGNAL("returnPressed()"), self.talkToRobot)
		QtCore.QObject.connect(self.ui.chatContextCheckbox, QtCore.SIGNAL("stateChanged(int)"), self.toggleChatContextVisible)
		
	def setActionsRobotState(self):
		QtCore.QObject.connect(self.ui.stateShowCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.toggleStateVisible)
		
	def setToolbarActions(self):
		self.connect(self.ui.exit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))
	
	def setTabActions(self):
		self.resetParameters()
		self.setActionsInterpolation()		
		self.setActionsResampling()
		self.setActionsMultiresfiltering()
	
	def setActionsGainSliders(self):
		print "setting actions for gain sliders and line edits...",
		for gs in self.ui.gainSliders:
			
			QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), self.adjustGain)

		for gle in self.ui.gainLineEdits:
			#print type(gle)
			QtCore.QObject.connect(gle, QtCore.SIGNAL("returnPressed()"), self.setSliderValue2)
		print "done!"
		
	def setActionsMultiresfiltering(self):
		print "setting actions for multiresolution filtering controls...",
		QtCore.QObject.connect(self.ui.mrfButton, QtCore.SIGNAL("clicked()"), self.multiresfilter)
		print "done!"
	
	def setActionsResampling(self):
		print "setting actions for resampling controls...",
		QtCore.QObject.connect(self.ui.resampButton, QtCore.SIGNAL("clicked()"), self.resample)
		print "done!"
	
	def setActionsMotionFile(self):
		QtCore.QObject.connect(self.ui.motionLoadButton, QtCore.SIGNAL("clicked()"), self.loadNewMotion)
		QtCore.QObject.connect(self.ui.khr1MotionRunButton, QtCore.SIGNAL("clicked()"), self.runKHR1Motion)
	
	def setActionsMotionControls(self):
		print "setting actions for motion controls...",
		QtCore.QObject.connect(self.ui.motionPlayButton, QtCore.SIGNAL("clicked()"), self.runMotion)
		QtCore.QObject.connect(self.ui.motionStopButton, QtCore.SIGNAL("clicked()"), self.stopMotion)
		QtCore.QObject.connect(self.ui.motionResetButton, QtCore.SIGNAL("clicked()"), self.resetData)
		print "done!"
	
	def setActionsAffectProcessingCheckBox(self):
		print "setting actions for Affect Processing checkbox...",
		QtCore.QObject.connect(self.ui.channelsAffectProcessingCheck, QtCore.SIGNAL("stateChanged(int)"), self.toggleAffectProcessing)
		print "done!"
	
	def setActionsChannelsCheckBox(self):
		print "setting actions for channel checkboxes...",
		for k,v in self.ui.channels.items():			
			QtCore.QObject.connect(v, QtCore.SIGNAL("stateChanged(int)"), self.toggleChannelVisible)
		print "done!"
	
	def setActionsInterpolation(self):
		QtCore.QObject.connect(self.ui.interpTensionSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateInterpParams)
		QtCore.QObject.connect(self.ui.interpBiasSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateInterpParams)
		QtCore.QObject.connect(self.ui.interpContinuitySpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateInterpParams)
		QtCore.QObject.connect(self.ui.interpButton, QtCore.SIGNAL("clicked()"), self.interpMotion)
		
	#------
	def toggleChatContextVisible(self, value):
		if value: 
			self.ui.chatContextGroupin.setVisible(True)
			self.writeToStatusBar("Displaying chat context")
		else:
			self.ui.chatContextGroupin.setVisible(False)
			self.writeToStatusBar("Hiding chat context")
	
	def toggleStateVisible(self, value):
		if value: 
			self.ui.stateGroup.setVisible(True)
			self.writeToStatusBar("Displaying robot state")
		else:
			self.ui.stateGroup.setVisible(False)
			self.writeToStatusBar("Hiding robot state")
		#print value, self.affectProcessing
	
	# ---		
	def talkToRobot(self):
		if self.dialogue.getName():
			response = self.dialogue.youSay('my name is '+self.dialogue.getName())
			self.ui.chatArea.append("<b><font color=blue>%s</font></b>" % (response))
		getUserInput = self.ui.chatInput.text()
		#print "Input: ", getUserInput, "type: ", type(str(getUserInput))
		getUserInput = str(getUserInput)
		
		if getUserInput in self.chatoptions.keys():
			response = self.dialogue.youSay(self.chatoptions[getUserInput])
			self.ui.chatArea.append("> %s" % (self.chatoptions[getUserInput]))
			self.scriptindex +=1
			userInput = self.chatoptions[getUserInput]
		else:
			response = self.dialogue.youSay(getUserInput)
			self.ui.chatArea.append("> %s" % (getUserInput))
			if getUserInput in [re for k,re in self.chatoptions.iteritems()]:
				self.scriptindex +=1
			userInput = getUserInput
					
		self.ui.chatArea.append("<b><font color=blue>>> %s</font></b>" % (response))
		
		self.ui.chatArea.append("<b><font color=green>Select your response:</font></b>")
		if self.scriptindex >= len(self.SCRIPT):
			self.scriptindex = 0
		
		scriptline = self.SCRIPT[self.scriptindex]
		
		for i in range(len(scriptline)):
			if scriptline[i] != '':
				self.ui.chatArea.append("<b><font color=green>%d.  %s</font></b>" % (i, scriptline[i]))
				self.chatoptions[str(i)] = scriptline[i]
		self.ui.chatArea.append("<b><font color=green>Or type anything ...</font></b><br>")
		self.ui.chatInput.clear()
		
		# LOCOCONTEXT PART
		print "before lcontext...%s, %s" % (response, getUserInput)
		
		# LOCOCONTEXT: try to extract context from user's input (getUserInput) & AIML response (response)
		(keyverb,emotion) = self.lcontext.lcKeywords(response, userInput)
		self.updateChatContext(keyverb,emotion)
		print "after lcontext..."
		#self.lcontext.lcKeywords(getUserInput,response)
		#self.lcontext.updateContext()
		(update,action,emotion,willingness) = self.lcontext.updateContext2()
		
		# write to UI: 'Robot Action' field
		if action is None:
			self.ui.robotAction.setText('None')
		else:
			self.ui.robotAction.setText(action)	
		
		# write to UI: 'Willingness' field	
		#~ self.ui.willingness.setText(str(willingness))
		self.ui.willingness.setValue(willingness)	# << using QwtThermo
		
		# print emotion levels to Terminal
		print "emotion:", self.lcontext.showEmos()
		
		# write to UI: emotion level fields		
		self.updateEmoState(self.lcontext.showEmos(), self.dialogueInit)
		self.dialogueInit = False
	   		
		# If the user say the name was wrong, redo face recognition
		if self.lcontext.wrongname():
			self.dialogue.recz()
		try:
			motion = self.lcontext.executeAllMotion()
			
			if motion:
				print "motion ready:"#, motion
				
				# Run the resulting motion from LocoContext
				khr1Interface(self.khr1device, motion).start()
				
			else: print "meh."
			
			#~ self.updateDialogueContextAction(response)
						
		except:
			print "Sorry, try again! Fix your LocoContext.executeAllMotion() function, or trouble with khr1Interface!"
		
		try:
			self.ui.statusbar.showMessage("I see "+self.dialogue.facedetect.faces+" face(s)")
		except:
			self.ui.statusbar.showMessage("I can't see anything...")
			
		
	
	# write to UI: Chat Context fields
	def updateChatContext(self, verb, emotion):
		self.ui.chatContextVerb.setText(str(verb))
		self.ui.chatContextEmo.setText(str(emotion))
			
	# write to UI: emotion level fields (called from talkToRobot(...))	
	def updateEmoState(self,emotions,init):
		#self.ui.happyLevel.setText(str(emotions['happy']))
		#self.ui.fearLevel.setText(str(emotions['fear']))
		#self.ui.sadnessLevel.setText(str(emotions['sad']))
		#self.ui.angerLevel.setText(str(emotions['anger']))
		self.ui.happyLevel.setValue(emotions['happy'])	# << using QwtThermo
		self.ui.fearLevel.setValue(emotions['fear'])	# << using QwtThermo
		self.ui.sadnessLevel.setValue(emotions['sad'])	# << using QwtThermo
		self.ui.angerLevel.setValue(emotions['anger'])	# << using QwtThermo
		if True:
			emolevel = [x for k,x in emotions.iteritems()]
			for k,x in emotions.iteritems():
				if x == max(emolevel):
					self.ui.robotMood.setText(k)
					self.setRobotPose(k)
					break
		else:
			self.setRobotPose('greet')
				
	def setRobotPose(self, pose):
		self.runMotion(motion=pose)		
	
	#------
	def setSliderValue2(self):
		index = int(self.sender().accessibleName())
		self.ui.gainSliders[index].setSliderPosition(int(self.ui.gainLineEdits[index].text())) 
	
	def adjustGain(self, value):
		gainIndex = int(self.sender().accessibleName())

		# === redraw
		
		#self.ms.multiresFiltering(self.checkCurrentData())
		self.ms.setDATA( self.checkCurrentData() )
		self.ms.multiresFiltering()		
		for i in range(self.ms.countGains()):
			for channel in range(self.channels):
				# === if it's not the changed slider...
				if i != gainIndex:
					if (self.affectProcessing and self.ui.channels[str(channel)].isChecked())or not self.affectProcessing:
						self.ms.adjustGain(channel, i, self.ui.gainSliders[i].value()*0.1)
						self.ui.gainLineEdits[i].setText(str(self.ui.gainSliders[i].value()*0.1))
					#else:
						#print "channel %d skipped" % channel
							
				# === otherwise, it's the changed slider	
				else:
					if (self.affectProcessing and self.ui.channels[str(channel)].isChecked())or not self.affectProcessing:
						self.ms.adjustGain(channel, gainIndex, value*0.1)
						self.ui.gainLineEdits[gainIndex].setText(str(self.ui.gainSliders[gainIndex].value()*0.1))
						self.writeToStatusBar("Band "+self.ui.gainSliders[gainIndex].accessibleName()+" gain changed to "+ str(value*0.1))
					#else:
						#print "channel %d skipped" % channel
				

		self.updatePlot()
		self.updateOutputData(self.ms.returnNewData())
		
		self.writeToStatusBar("Sender: %s, value: %f" % (self.sender().accessibleName(), self.sender().value()*0.1))#, self.tmpData[channel]
		#self.ms.DATA = self.ms.returnNewData()
	
	def checkCurrentData(self):
		if len(self.CURRENT_MOTION_DATA[0]) >= 8 and self.CURRENT_INTERP_MOTION_DATA == []:
			print "using CURRENT_MOTION_DATA...",
			#banddata = self.ms.multiresFiltering(self.CURRENT_MOTION_DATA)
			filterdata = self.CURRENT_MOTION_DATA
		elif len(self.CURRENT_INTERP_MOTION_DATA[0]) >= 8:
			print "using CURRENT_INTERP_MOTION_DATA...",
			#banddata = self.ms.multiresFiltering(self.CURRENT_INTERP_MOTION_DATA)
			filterdata = self.CURRENT_INTERP_MOTION_DATA
		else:
			print "need length of motion data > 8"
			return 0
		return filterdata
	
	def multiresfilter(self):
		try:
			print "filtering...",
			"""if len(self.CURRENT_MOTION_DATA[0]) >= 8 and self.CURRENT_INTERP_MOTION_DATA == []:
				print "using CURRENT_MOTION_DATA...",
				banddata = self.ms.multiresFiltering(self.CURRENT_MOTION_DATA)
			elif len(self.CURRENT_INTERP_MOTION_DATA[0]) >= 8:
				print "using CURRENT_INTERP_MOTION_DATA...",
				banddata = self.ms.multiresFiltering(self.CURRENT_INTERP_MOTION_DATA)
			else:
				print "need length of motion data > 8"
				return 0
			"""
			filterdata = self.checkCurrentData()
			banddata = self.ms.multiresFiltering(filterdata)
			#print "I get: ", banddata
			#self.channels = len(self.ms.DATA)
			self.resetToolTabs()	   
			self.ui.addGainSliders(len(banddata[0]))
			#self.setTabActions()
			self.setActionsGainSliders()
		except:
			print "multiresfilter() failed:"
			
	def resample(self):
		try:
			print "sampling..."
			resample = resampling.resample
			rate = self.ui.resampRateSpinBox.value()
			#resampddata = [resample(data, rate) for data in self.CURRENT_INTERP_MOTION_DATA]
			resampddata = [resample(data, rate) for data in self.OUTPUT_DATA]
			#self.ms.multiresFiltering(new_data)
			#self.updatePlot()
			self.plotMotion(resampddata)
			self.updateCurrentInterpMotionData(resampddata)
			self.updateOutputData(resampddata)			
			print "done!"
		except:
			print "resample() failed."
			return 0 		
	
	def stopMotion(self):
		try:
			self.k1.togglethread()
			print "KHR1 thread killed"
		except:
			print "Unable to kill KHR1 thread"
	
	def runMotion(self, motion=None):
		try:
			#if self.CURRENT_INTERP_MOTION_DATA != []:
			#	motion = self.CURRENT_INTERP_MOTION_DATA
			#else: motion = self.CURRENT_MOTION_DATA
			if motion is None:
				motion = self.OUTPUT_DATA
						
			self.k1 = khr1Interface(self.khr1Device, motion)
			self.k1.start()
			#self.k1.runMe(motion)
			#self.kk = khr1I()
		except:
			print "runMotion() failed."		
		
	def updateInterpParams(self, value):
		callerID = str(self.sender().accessibleName())
		#print "Param: %s" % (callerID)
		#print "Old value: %f" % (self.interpParameters[callerID]),
		v = value*.1
		self.interpParameters[callerID] = value*.1
		self.writeToStatusBar(callerID+" value:"+str(v))
		#print "New value: %f" % (self.interpParameters[callerID])	
		
	def interpMotion(self):
		print "interpolating...",
		try:
			# Call interpolation method from MotionSynthesizer class
			interpData = self.ms.interpolate(self.CURRENT_MOTION_DATA, 
											 self.interpParameters['bias'], 
											 self.interpParameters['tension'], 
											 self.interpParameters['continuity'])
			self.plotMotion(interpData)	# plot the new data
			print "success!"
			
			self.updateCurrentInterpMotionData(interpData)	# update self.CURRENT_INTERP_MOTION_DATA
			self.updateOutputData(interpData)
		except:
			print "interpMotion() failed"
			return 0
	
	def toggleAffectProcessing(self, value):
		if value: 
			self.affectProcessing = True
			self.writeToStatusBar("Selective channel processing")
		else:
			self.affectProcessing = False
			self.writeToStatusBar("All channel processing")
		print value, self.affectProcessing
		
	
	def toggleChannelVisible(self, value):
		ix = self.sender().accessibleName()		
		if value: value = True
		self.ui.motionPlot.toggleVisible(int(ix), value)
		
	def resetData(self):
		motion = self.ui.motionComboBox.currentText()
		print "Resetting data..."
		self.ui.motionPlot.reInitialize()
		self.loadData(dataIndex=motion)
		self.CURRENT_INTERP_MOTION_DATA = []
		self.writeToStatusBar("Motion: %s reset." % (motion))
		self.resetToolTabs()
		#self.ui.initToolTabs()
		#self.setTabActions()
		
	def resetParameters(self):
		self.interpParameters['tension'] = 0
		self.interpParameters['bias'] = 0
		self.interpParameters['continuity'] = 0
		self.channels=24
		
	def resetToolTabs(self):
		self.ui.initToolTabs()
		self.setTabActions()
		
	def runKHR1Motion(self):
		id = int(self.ui.khr1MotionComboBox.currentText())
		print id
		self.k1 = khr1Interface(self.khr1Device, id)
		self.k1.start()
	
	def loadNewMotion(self):
		motion = self.ui.motionComboBox.currentText()
		print "Load new motion..."
		print "New motion: %s" % (motion)
		self.ui.motionPlot.reInitialize()
		self.loadData(dataIndex=motion)
		self.CURRENT_INTERP_MOTION_DATA = []
		self.writeToStatusBar("Motion: %s loaded." % (motion))
		self.resetToolTabs()
		
		#self.ui.initToolTabs()		
		
	def loadMotionFiles(self):		
		return glob.glob(self.defaultMotionPath+"*.csv")   # <<< List of all motion files
		
	def formatMotionList(self, motionList):		
		pathname = re.compile('(\/home\/msunardi\/Documents\/thesis\-stuff\/KHR\-1\-motions)\/((\w*)(\D*)(\w*)).csv', re.IGNORECASE)
		for path in motionList:
			name = pathname.match(path).group(2)
			self.motionSignalPath[name] = path
	
	def updateOutputData(self, data):
		self.OUTPUT_DATA = data
		self.writeToStatusBar("OUTPUT_DATA updated.")
			
	def updateCurrentMotionData(self, motiondata):
		self.CURRENT_MOTION_DATA = motiondata
		print "CURRENT_MOTION_DATA updated."
		self.writeToStatusBar("CURRENT_MOTION_DATA updated.")
		
	def updateCurrentInterpMotionData(self, motiondata):
		self.CURRENT_INTERP_MOTION_DATA = motiondata
		print "CURRENT_INTERP_MOTION_DATA updated."
		self.writeToStatusBar("CURRENT_INTERP_MOTION_DATA updated.")
	
	#-----
	def writeToStatusBar(self, message):
		self.ui.statusbar.showMessage(message)
	
	def updatePlot(self):
		for channel in range(self.channels):
			if self.affectProcessing and self.ui.channels[str(channel)].isChecked():
				self.ui.motionPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))
			elif not self.affectProcessing:
				self.ui.motionPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))
	
	def plotMotion(self, plotdata):
		ch = 0
		self.ui.motionPlot.reInitialize()				# initialize plot object
		for i in plotdata:
			self.ui.motionPlot.addCurve(i) 				# plot each channel
			self.ui.motionPlot.toggleVisible(ch, self.ui.channels[str(ch)].isChecked()) # use this line when checkbox data is dictionary
			#self.ui.motionPlot.toggleVisible(ch, self.ui.channels[ch].isChecked())	# use this line when checkbox data is a list
			ch += 1
	
	def loadData(self, dataIndex):		
		try:
			# === Read data
			#dataPath = self.motionSignalPath[self.ui.motionComboBox.currentIndex()]		# get path to motion file
			dataIndex = str(dataIndex)
			dataPath = self.motionSignalPath[dataIndex]	# get path to motion file
			motionData = self.ms.read(dataPath)			# read motion file
			print "loadData(): motion data loaded."
			self.ui.motionPlot.reInitialize()			# initialize plot object
			self.plotMotion(plotdata=motionData)		# plot loaded motion data
			
			self.updateCurrentMotionData(motionData)
			self.updateOutputData(motionData)
		except:
			print "loadData(dataPath) failure: Need some path to a valid data"
			return 0
		
		self.ui.motionTabs.setTabText(0,self.ui.motionComboBox.currentText())
		"""# === PLOT TITLE
		self.ms.DATA = self.ms.interpolate(self.originalData, self.interpBias, self.interpTension, self.interpContinuity)
		self.freqBands = self.ms.multiresFiltering()
		
		print "Data loaded"

		# === Apply filter
		# CAUTION!!!  self.originalData is local to this class...
		#	... another data already exist within MotionSynthesizer object: self.ms
		#	... the internal self.ms data can be accessed as: self.ms.DATA
		#	All operations on data should be done on the internal (self.ms.DATA)
		#	This local data (self.originalData) may be used to reset the internal data
		#

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
		"""

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())
