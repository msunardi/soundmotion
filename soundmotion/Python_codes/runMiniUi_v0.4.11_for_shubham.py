#!/usr/bin/env python
#
#       runMiniUi_v0.4.11_for_shubham.py
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

## Load necessary libraries...
import sys, glob, re, resampling	# << load some libraries:
									# sys: to tell Python to look for certain paths in the Local Drive (directories)
									# glob: a Python library to read and load the contents of a directory
									# re: the Python Regular Expressions library
									# resampling: my code for the (Re)Sampling function... you can ignore this for now
import PyQt4.Qwt5 as Qwt		# << Load the Qwt library to plot graphs
from PyQt4 import QtCore, QtGui, Qt		# << load the necessary Qt libraries
from pyMiniUix_v10 import Ui_MainWindow		# << load the user-interface object "Ui_MainWindow" from file: "pyMiniUix_v10.py"
#from mosynth20_p import MotionSynthesizer		# << load the signal processing object "MotionSynthesizer" from file: "mosynth20_p.py"
#from locoKHR1Interface_v8 import khr1Interface	# << load the object "khr1Interface" (handles serial interface with KHR-1) from file: "locoKHR1Interface_v8.py"
#from dialogueModule import Dialogue
#from LocoContext15 import locoContext
#from scriptReadCsv import readScript

class MyForm(QtGui.QMainWindow):	# << the class MyForm inherits from the class QtGui.QMainWindow
		
	def __init__(self, parent=None):	# << initialization of the class MyForm
		QtGui.QWidget.__init__(self, parent)	# << because the class MyForm inherits from the class QtGui.QMainWindow, the parent class (QtGui.QMainWindow) must be initialized as well
		self.ui = Ui_MainWindow()	# << instansiate the class Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.setVariables()		# << function call to setVariables() -- setting up some global variables that will be used throughout the program
		
		self.ui.populateChannelList()	# << create/draw the checkboxes for the list of channels (seen under the label "Channel Visibility")
		self.setActions()				# << set the actions/function calls for each component in the user interface (for example: what happens when user click the OK button)
		self.motionPath = self.loadMotionFiles()	# << set the path/directory name for the motion files (saved in .csv format)
		
		self.formatMotionList(self.motionPath)		# << format the pathnames for the motion files so they are easier to read
		
		self.ui.populateKhr1MotionBox()				# << calls the "populateKhr1MotionBox()" function in Ui_MainWindow class to populate the dropdown tool with numbers 0 - 39 (indexes of the motions in KHR-1's memory)
		
		#self.ui.populateMotionBox(self.formatMotionList(self.motionSignalPath))		
		self.ui.populateMotionBox([k for k,v in self.motionSignalPath.items()])		# << calls the "populateMotionBox(...)" function in Ui_MainWindow class to populate the dropdown tool with names of the motion files
		#self.loadData(self.motionSignalPath[self.ui.motionComboBox.currentIndex()])
		print self.ui.motionComboBox.currentText()		# << prints the current selected motion name on screen
		#self.loadData(self.motionSignalPath[self.ui.motionComboBox.currentText()])
		self.loadData(dataIndex=self.ui.motionComboBox.currentText())	# << load the selected motion data, and display it as a graph
		
	def setVariables(self):
		# Containers...
		self.motionPath = []	# list of path to .csv files loaded using glob
		self.motionSignalPath = {}	# dictionary of path to .csv files indexed by file name		
		self.CURRENT_MOTION_DATA = []	# container for current loaded motion data from file
		self.CURRENT_INTERP_MOTION_DATA = []	# container for current interpolated motion data
		self.OUTPUT_DATA = []		# container for the final motion data that will be sent to KHR-1
		#self.SCRIPT = []			# container for chat scripts -- (Shubham: you can ignore this for now)
		#self.chatoptions = {}		# another container for chat scripts -- (Shubham: you can ignore this for now)
		
		# Parameters...
		self.interpParameters = {'tension': 0, 'bias': 0, 'continuity': 0}	# interpolation parameters
		self.affectProcessing = False		# << True/False flag to set if Channel Visibility affects selective channel processing/filtering
		self.dialogueInit = True			# << flag to indicate that the conversation just started
		#self.usewillingness = True			# << flag to indicate to use/not use the "Willingness" value (Shubham: you can ignore this for now)
		
		# Constants...
		self.defaultMotionPath = "KHR-1-motions/"  	# << this is the path for the motion files (.csv) 
		self.khr1Device = "/dev/ttyUSB0"			# << this is the serial port object (in Windows, this would be like: COM1, COM2, etc.)
		#scriptpath = 'scripts/script1.csv'			# << this is the path to the chat script (Shubham: you can ignore this for now)
		
		# Class instances... (Shubham: I disabled these following parts for now...)
		"""
		self.ms = MotionSynthesizer()			# << instantiate the signal processing class
		
		try:
			self.dialogue = Dialogue()			# << try to instantiate the dialogue module
		except:
			print "No dialogue this time..."	# << if something is wrong or the dialogue module cannot be instantiated, print this

		try:
			self.lcontext = locoContext()		# << try to instantiate the context module
		except:
			print "No lococontext this time..."	# << if something is wrong or the context module cannot be instantiated, print this
			
		try:
			rs = readScript()					# << instantiate the class to read the chat script
			self.SCRIPT = rs.read(scriptpath)
			print "Script: %s is loaded." % scriptpath
			self.scriptindex=0
		except:
			print "Failed loading Script."
		"""
	
	# Setting actions for the user interface components	
	def setActions(self):
		print "setActions"
		
		self.setActionsChannelsCheckBox()			# << set actions for the channel checkboxes
		self.setActionsAffectProcessingCheckBox()	# << set action for the "Affect Processing" checkbox
		self.setActionsMotionControls()				# << set actions for the buttons in the "Motion Controls" group
		self.setActionsMotionFile()					# << set actions for the buttons in the "Motion File" group
		
		self.setTabActions()						# << set actions for the signal processing interface components
		self.setToolbarActions()					# << set actions for the toolbar buttons
		self.setActionsRobotState()					# << set actions for the "show/hide" robot state checkbox and "use willingness" checkbox
		self.setActionsChatUI()						# << set actions for the chat interface components
		
	# Set actions for the chat interface components
	def setActionsChatUI(self):
		# Setting actions for a Qt component is by using "connect SIGNAL to SLOT" concept,
		# SIGNAL means the actions the user do to the interface component.  For example: a button is 'clicked'
		# SLOT means what happens after the SIGNAL is sent.  For example: close a window.
		
		# If the QButton "chatInputClearButton" is clicked <SIGNAL: "clicked()">, clear <SLOT: "clear()"> the text in the QLineEdit "chatInput"
		QtCore.QObject.connect(self.ui.chatInputClearButton, QtCore.SIGNAL("clicked()"), self.ui.chatInput, QtCore.SLOT("clear()"))
		
		# If the QButton "chatInputEnterButton" is clicked <SIGNAL: "clicked()">, call the "talkToRobot()" function.
		QtCore.QObject.connect(self.ui.chatInputEnterButton, QtCore.SIGNAL("clicked()"), self.talkToRobot)
		
		# If after typing in a sentence in the QLineEdit "chatInput", the user pressed the "Enter" key, call the "talkToRobot()" function
		QtCore.QObject.connect(self.ui.chatInput, QtCore.SIGNAL("returnPressed()"), self.talkToRobot)
		
		# If the QCheckBox "chatContextCheckbox" is checked/unchecked, call the "toggleChatContextVisible" function.
		QtCore.QObject.connect(self.ui.chatContextCheckbox, QtCore.SIGNAL("stateChanged(int)"), self.toggleChatContextVisible)
		
	# Set actions for the "show/hide" robot state checkbox and "use willingness" checkbox
	def setActionsRobotState(self):
		QtCore.QObject.connect(self.ui.stateShowCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.toggleStateVisible)
		QtCore.QObject.connect(self.ui.useWillingnessCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.toggleUseWillingness)
		
	# Set actions for the toolbar buttons
	def setToolbarActions(self):
		self.connect(self.ui.exit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))
	
	# Set actions for the signal processing interface components
	def setTabActions(self):
		self.resetParameters()
		self.setActionsInterpolation()		
		self.setActionsResampling()
		self.setActionsMultiresfiltering()
	
	# Set actions when the sliders objects for the filtering gains are moved, or the values changed
	def setActionsGainSliders(self):
		print "setting actions for gain sliders and line edits...",
		for gs in self.ui.gainSliders:
			
			QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), self.adjustGain)

		for gle in self.ui.gainLineEdits:
			#print type(gle)
			QtCore.QObject.connect(gle, QtCore.SIGNAL("returnPressed()"), self.setSliderValue2)
		print "done!"
		
	# Set actions when the QButton "mrfButton" (text: "Multiresfiltering!") is clicked
	def setActionsMultiresfiltering(self):
		print "setting actions for multiresolution filtering controls...",
		QtCore.QObject.connect(self.ui.mrfButton, QtCore.SIGNAL("clicked()"), self.multiresfilter)
		print "done!"
	
	# Set actions when the QButton "resampButton" (text: "Resampling") is clicked
	def setActionsResampling(self):
		print "setting actions for resampling controls...",
		QtCore.QObject.connect(self.ui.resampButton, QtCore.SIGNAL("clicked()"), self.resample)
		print "done!"
	
	# Set actions for the QButtons in the "Motion File" group
	def setActionsMotionFile(self):
		QtCore.QObject.connect(self.ui.motionLoadButton, QtCore.SIGNAL("clicked()"), self.loadNewMotion)
		QtCore.QObject.connect(self.ui.khr1MotionRunButton, QtCore.SIGNAL("clicked()"), self.runKHR1Motion)
	
	# Set actions for the QButtons in the "Motion Controls" group
	def setActionsMotionControls(self):
		print "setting actions for motion controls...",
		QtCore.QObject.connect(self.ui.motionPlayButton, QtCore.SIGNAL("clicked()"), self.runMotion)
		QtCore.QObject.connect(self.ui.motionStopButton, QtCore.SIGNAL("clicked()"), self.stopMotion)
		QtCore.QObject.connect(self.ui.motionResetButton, QtCore.SIGNAL("clicked()"), self.resetData)
		print "done!"
	
	# Set actions when the checkbox "channelsAffectProcessingCheck" (Affect Processing checkbox) is checked/unchecked
	def setActionsAffectProcessingCheckBox(self):
		print "setting actions for Affect Processing checkbox...",
		QtCore.QObject.connect(self.ui.channelsAffectProcessingCheck, QtCore.SIGNAL("stateChanged(int)"), self.toggleAffectProcessing)
		print "done!"
	
	# Set actions for each channel checkbox
	def setActionsChannelsCheckBox(self):
		print "setting actions for channel checkboxes...",
		for k,v in self.ui.channels.items():			
			QtCore.QObject.connect(v, QtCore.SIGNAL("stateChanged(int)"), self.toggleChannelVisible)
		print "done!"
	
	# Set actions for the interpolation interface components
	def setActionsInterpolation(self):
		QtCore.QObject.connect(self.ui.interpTensionSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateInterpParams)
		QtCore.QObject.connect(self.ui.interpBiasSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateInterpParams)
		QtCore.QObject.connect(self.ui.interpContinuitySpinBox, QtCore.SIGNAL("valueChanged(int)"), self.updateInterpParams)
		QtCore.QObject.connect(self.ui.interpButton, QtCore.SIGNAL("clicked()"), self.interpMotion)
		
	#------
	def toggleUseWillingness(self, value):	# a little tricky here... "value" is an integer value being sent by 
											# the willingness checkbox but is not explicitly shown 
											# when the function is called (see Line 140).
											# The toggleUseWillingness function just expects it will receive an
											# integer value when the checkbox object is clicked/toggled.
											# All checkbox objects behave this way in Qt.
		if value: 			# if the checkbox is checked
			self.writeToStatusBar("Use Willingness")
			self.usewillingness = True
		else:				# otherwise... (if the checkbox is unchecked)
			self.writeToStatusBar("Ignore Willingness")
			self.usewillingness = False
	
	# Show/hide the chatContextGroupin object ("Chat Context" group in the Chat UI)
	def toggleChatContextVisible(self, value):
		if value: 
			self.ui.chatContextGroupin.setVisible(True)
			self.writeToStatusBar("Displaying chat context")
		else:
			self.ui.chatContextGroupin.setVisible(False)
			self.writeToStatusBar("Hiding chat context")
	
	# Show/hide the stateGroup object ("Robot State" group in the Chat UI)
	def toggleStateVisible(self, value):
		if value: 
			self.ui.stateGroup.setVisible(True)
			self.writeToStatusBar("Displaying robot state")
		else:
			self.ui.stateGroup.setVisible(False)
			self.writeToStatusBar("Hiding robot state")
		#print value, self.affectProcessing
	
	# ---
	# THE FUNCTIONS BELOW ARE THE MAIN FEATURES/FUNCTIONALITIES OF THE USER INTERFACE
	# ---
	
	# talkToRobot:
	# Usage:
	#		To process user's input sentence by:
	#			1. Sending it to the ALICE chat client
	#			2. Extracting context/keywords from it.  This will:
	#					- change the robot's 'mood'
	#					- determine the action/movement to be executed by the robot
	#		User's input sentence is directly read from the "chatInput" QLineEdit object
	#		Result:
	#			- ALICE's text response (displayed on the QTextBrowser "chatArea")
	#			- extracted emotive & action keywords
	#			- robot's mood levels (also updates the components in the UI in the group "Robot State")
	# Input arguments:
	#		None
	# Returns:
	#		None
	#		
	def talkToRobot(self):
		#if self.dialogue.getName():
		#	response = self.dialogue.youSay('my name is '+self.dialogue.getName())
		#	self.ui.chatArea.append("<b><font color=blue>%s</font></b>" % (response))
		
		getUserInput = self.ui.chatInput.text()			# << read user's input from the QLineEdit "chatInput"
		getUserInput = str(getUserInput)				# << convert it to string...
		self.ui.chatArea.append("> %s" % (getUserInput))
		
		"""if getUserInput in self.chatoptions.keys():
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
		"""
		self.ui.chatInput.clear()
		
		# LOCOCONTEXT PART
		#-print "before lcontext...%s, %s" % (response, getUserInput)
		
		# LOCOCONTEXT: try to extract context from user's input (getUserInput) & AIML response (response)
		#-(keyverb,emotion) = self.lcontext.lcKeywords(response, userInput)
		#-self.updateChatContext(keyverb,emotion)
		#-print "after lcontext..."		
		#-(update,action,emotion,willingness) = self.lcontext.updateContext2(self.usewillingness)
		
		# write to UI: 'Robot Action' field
		#~ if action is None:
			#~ self.ui.robotAction.setText('None')
		#~ else:
			#~ self.ui.robotAction.setText(action)	
		
		# write to UI: 'Willingness' field	
		#~ self.ui.willingness.setText(str(willingness))
		#~ self.ui.willingness.setValue(willingness)	# << using QwtThermo
		
		# print emotion levels to Terminal
		#~ print "emotion:", self.lcontext.showEmos()
		#~ print "robotaction:", action
		
		# write to UI: emotion level fields		
		#~ self.updateEmoState(self.lcontext.showEmos(), self.dialogueInit, action)
		self.dialogueInit = False
	   		
		# If the user say the name was wrong, redo face recognition
		#~ if self.lcontext.wrongname():
			#~ self.dialogue.recz()
		"""try:
			motion = self.lcontext.executeAllMotion()
			
			if motion:
				print "motion ready:", type(motion)
				
				# Run the resulting motion from LocoContext
				#khr1Interface(self.khr1device, motion).start()
				self.runMotion(motion)
				
			else: print "meh."
			
			#~ self.updateDialogueContextAction(response)
						
		except:
			print "Sorry, try again! Fix your LocoContext.executeAllMotion() function, or trouble with khr1Interface!"
		
		try:
			self.ui.statusbar.showMessage("I see "+self.dialogue.facedetect.faces+" face(s)")
		except:
			self.ui.statusbar.showMessage("I can't see anything...")
		"""	
		
	"""
	# write to UI: Chat Context fields
	def updateChatContext(self, verb, emotion):
		self.ui.chatContextVerb.setText(str(verb))
		self.ui.chatContextEmo.setText(str(emotion))
	"""
	"""		
	# write to UI: emotion level fields (called from talkToRobot(...))	
	def updateEmoState(self,emotions,init,action):
		print "UPDATEEMOSTATE: action:", action, type(action)
		self.ui.happyLevel.setValue(emotions['happy'])	# << using QwtThermo
		self.ui.fearLevel.setValue(emotions['fear'])	# << using QwtThermo
		self.ui.sadnessLevel.setValue(emotions['sad'])	# << using QwtThermo
		self.ui.angerLevel.setValue(emotions['anger'])	# << using QwtThermo
		#if True:
		emolevel = [x for k,x in emotions.iteritems()]
		for k,x in emotions.iteritems():
			if emolevel.count(0.25) == 4 and str(action) == 'None':
				self.setRobotPose('happy')
				self.ui.robotMood.setText('happy')
				break
			elif x == max(emolevel):
				self.ui.robotMood.setText(k)
				if str(action) == 'None':
					self.setRobotPose(k)
				break
		#else:
		#	self.setRobotPose('greet')
	"""			
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
	
	# checkCurrentData:
	# Usage:
	#		to determine which data to filter
	# Input arguments:
	#		None
	# Returns:
	#		motion data to be filtered
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
	
	# multiresfilter:
	# Usage:
	#		Filters the provided motion data
	#		Will create appropriate number of gain sliders (depends on how long the data is)
	#		Will also reinitialize the signal processing UI
	# Input arguments:
	#		None
	# Returns:
	#		None
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
			
	# resample:
	# Usage:
	#		Resample the current motion data
	#		Sampling rate is read from the QSpinBox object "resampRateSpinBox"
	#		the result of the resampling will be stored in the self.OUTPUT_DATA variable
	# Input arguments:
	#		None
	# Returns:
	# 		None
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
	
	# stopMotion:
	# Usage:
	# 		to kill the thread that execute motions on KHR-1
	# Input arguments:
	# 		None
	# Returns:
	#		None
	def stopMotion(self):
		try:
			self.k1.togglethread()
			print "KHR1 thread killed"
		except:
			print "Unable to kill KHR1 thread"
	
	# runMotion:
	# Usage:
	#		to execute motions on KHR-1 by creating a new Python thread
	# Input arguments:
	#		- motion: this can be in the following types:
	#				- int: will run a motion from KHR-1's on-board memory
	#				- list: will send servo positions sequentially
	#				- string: will run a KHR-1's scenario
	# Returns:
	#		None
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
		
	# updateInterpParams:
	# Usage:
	#		set the values for the interpolation parameters
	# Input arguments:
	#		- value: the int value being sent from the corresponding interpolation parameter input objects
	#			Note: similar to the checkbox in Line 211, "value" is being sent implicitly by the input objects
	# Returns:
	#		None
	def updateInterpParams(self, value):
		callerID = str(self.sender().accessibleName())	# << get the name of the object sending the value
		#print "Param: %s" % (callerID)
		#print "Old value: %f" % (self.interpParameters[callerID]),
		v = value*.1									# << "value" is always integer, but we want it to be float
		self.interpParameters[callerID] = value*.1		# << self.interpParameters is a Python 'Dictionary' type.
														# << the elements are indexed by the interpolation parameter names: 'Continuity', 'Tension', and 'Bias'
		self.writeToStatusBar(callerID+" value:"+str(v))
		#print "New value: %f" % (self.interpParameters[callerID])	
	
	# interpMotion:
	# Usage:
	#		execute interpolation to the motion data
	# Input arguments:
	#		None
	# Returns:
	#		None	
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
	
	# toggleAffectProcessing:
	# Usage:
	#		to set whether or not changing the visibility of a channel determines if gain adjustments
	#		from multiresolution filtering will affect the channel
	# Input arguments:
	#		- value: the integer value sent by the "Affect Processing" QCheckBox (similar to Line 211)
	# Returns:
	#		None
	def toggleAffectProcessing(self, value):
		if value: 
			self.affectProcessing = True
			self.writeToStatusBar("Selective channel processing")
		else:
			self.affectProcessing = False
			self.writeToStatusBar("All channel processing")
		print value, self.affectProcessing
		
	
	# toggleChannelVisible:
	# Usage:
	#		to change the visibility of each channel shown in the graph
	# Input parameters:
	#		- value: the integer value sent by the channel checkboxes (similar to Line 211)
	# Returns:
	#		None
	def toggleChannelVisible(self, value):
		ix = self.sender().accessibleName()		
		if value: value = True
		self.ui.motionPlot.toggleVisible(int(ix), value)
		
	# resetData:
	# Usage:
	#		to reset the motion data to its original form (before any signal processing)
	# Input arguments:
	#		None
	# Returns:
	#		None
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
		
	# resetParameters:
	# Usage:
	#		to reset the interpolation parameter values to 0
	# Input parameters:
	#		None
	# Returns:
	#		None
	def resetParameters(self):
		self.interpParameters['tension'] = 0
		self.interpParameters['bias'] = 0
		self.interpParameters['continuity'] = 0
		self.channels=24
		
	# resetToolTabs:
	# Usage:
	#		to reset the signal processing tools UI
	#		For example: you want to start over after many complicated modifications to the motion data
	# Input arguments:
	#		None
	# Returns:
	#		None
	def resetToolTabs(self):
		self.ui.initToolTabs()
		self.setTabActions()
	
	# runKHR1Motion:
	# Usage:
	#		- Run a motion from KHR-1 on-board memory
	#		- Creates a new Python thread
	#		- the motion index is retrieved from the QComboBox "khr1MotionComboBox"
	# Input arguments:
	#		None
	# Returns:
	#		None	
	def runKHR1Motion(self):
		id = int(self.ui.khr1MotionComboBox.currentText())
		print id
		self.k1 = khr1Interface(self.khr1Device, id)
		self.k1.start()
	
	# loadNewMotion:
	# Usage:
	#		load KHR-1 motion data from file
	# Input arguments:
	#		None
	# Returns:
	#		None
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
	
	# loadMotionFiles:
	# Usage:
	#		read all existing the motion files in the directory path given in "self.defaultMotionPath"
	# Input arguments:
	#		None
	# Returns:
	#		List of all the motion files (files that has extension ".csv")
	def loadMotionFiles(self):		
		return glob.glob(self.defaultMotionPath+"*.csv")   # <<< List of all motion files
		
	# formatMotionList:
	# Usage:
	#		- store the paths of the motion files in a Python 'Dictionary' "self.motionSignalPath"
	#		- the paths to the motion files are indexed in the "self.motionSignalPath" Dictionary by their file names (without the .csv extension)
	# Input arguments:
	#		- motionList: list of paths for all the motion files
	# Returns:
	#		None
	def formatMotionList(self, motionList):		
		pathname = re.compile('(\/home\/msunardi\/Documents\/thesis\-stuff\/KHR\-1\-motions)\/((\w*)(\D*)(\w*)).csv', re.IGNORECASE)
		for path in motionList:
			name = pathname.match(path).group(2)
			self.motionSignalPath[name] = path
	
	# updateOutputData:
	# Usage:
	#		- update the final motion data container (self.OUTPUT_DATA)
	#		- self.OUTPUT_DATA is always the motion data that will be executed on the KHR-1 (unless the user wants to run a motion in KHR-1's onboard memory)
	# Input arguments:
	#		- data: the new motion data
	# Returns:
	#		None
	def updateOutputData(self, data):
		self.OUTPUT_DATA = data
		self.writeToStatusBar("OUTPUT_DATA updated.")
	
	# updateCurrentMotionData:
	# Usage:
	#		- update the original motion data container (self.CURRENT_MOTION_DATA) everytime user load a motion data from file
	#		- self.CURRENT_MOTION_DATA should always contain the original/unmodified motion data loaded from file
	#		- Any interpolation, resampling or filtering gain adjustments shouldn't change this data.	
	# Input arguments:
	#		- motiondata: should always be the motion data loaded from file
	# Returns:
	#		None		
	def updateCurrentMotionData(self, motiondata):
		self.CURRENT_MOTION_DATA = motiondata
		print "CURRENT_MOTION_DATA updated."
		self.writeToStatusBar("CURRENT_MOTION_DATA updated.")
	
	# updateCurrentInterpMotionData:
	# Usage:
	#		- update the current interpolated motion data container (self.CURRENT_INTERP_MOTION_DATA)
	#		- self.CURRENT_INTERP_MOTION_DATA always contains the interpolated motion data.  Any resampling or filtering gain adjustments shouldn't change this data.
	#		- self.CURRENT_INTERP_MOTION_DATA should be updated if user re-interpolate the motion data
	# Input arguments:
	#		- motiondata: the new interpolated motion data
	# Returns:
	#		None
	def updateCurrentInterpMotionData(self, motiondata):
		self.CURRENT_INTERP_MOTION_DATA = motiondata
		print "CURRENT_INTERP_MOTION_DATA updated."
		self.writeToStatusBar("CURRENT_INTERP_MOTION_DATA updated.")
	
	#-----
	# writeToStatusBar:
	# Usage:
	#		to display a message on the status bar (bottom of window)
	# Input arguments:
	#		message: the message to display
	# Returns:
	#		None
	def writeToStatusBar(self, message):
		self.ui.statusbar.showMessage(message)
	
	# updatePlot:
	# Usage:
	#		to update the motion graph after modifications to the motion data
	#		the new modified motion data is retrieved from the signal processing module (MotionSynthesizer) (see Line 31)
	# Input arguments:
	#		None
	# Returns:
	#		None
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
	
	# Load the selected motion name
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
		

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())

