import sys, glob, re, resampling

import PyQt4.Qwt5 as Qwt
from PyQt4 import QtCore, QtGui, Qt
from pyMiniUix_v3 import Ui_MainWindow
from mosynth17_p import MotionSynthesizer
from locoKHR1Interface import khr1Interface

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
		
		# Parameters...
		self.interpParameters = {'tension': 0, 'bias': 0, 'continuity': 0}	# interpolation parameters
		self.affectProcessing = False
		
		# Constants...
		self.defaultMotionPath = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/"
		self.khr1Device = "/dev/ttyUSB0"
		
		# Class instances...
		self.ms = MotionSynthesizer()		
		
	def setActions(self):
		print "setActions"
		
		self.setActionsChannelsCheckBox()
		self.setActionsAffectProcessingCheckBox()		
		self.setActionsMotionControls()
		QtCore.QObject.connect(self.ui.motionLoadButton, QtCore.SIGNAL("clicked()"), self.loadNewMotion)
		self.setTabActions()
	
	def setTabActions(self):
		self.setActionsInterpolation()		
		self.setActionsResampling()
		self.setActionsMultiresfiltering()
		
	def setActionsMultiresfiltering(self):
		print "setting actions for multiresolution filtering controls...",
		QtCore.QObject.connect(self.ui.mrfButton, QtCore.SIGNAL("clicked()"), self.multiresfilter)
		print "done!"
	
	def setActionsResampling(self):
		print "setting actions for resampling controls...",
		QtCore.QObject.connect(self.ui.resampButton, QtCore.SIGNAL("clicked()"), self.resample)
		print "done!"
	
	def setActionsMotionControls(self):
		print "setting actions for motion controls...",
		QtCore.QObject.connect(self.ui.motionPlayButton, QtCore.SIGNAL("clicked()"), self.runMotion)
		QtCore.QObject.connect(self.ui.motionStopButton, QtCore.SIGNAL("clicked()"), self.stopMotion)
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
	def multiresfilter(self):
		try:
			print "filtering...",
			if len(self.CURRENT_MOTION_DATA[0]) >= 8 and self.CURRENT_INTERP_MOTION_DATA == []:
				print "using CURRENT_MOTION_DATA...",
				banddata = self.ms.multiresFiltering(self.CURRENT_MOTION_DATA)
			elif len(self.CURRENT_INTERP_MOTION_DATA[0]) >= 8:
				print "using CURRENT_INTERP_MOTION_DATA...",
				banddata = self.ms.multiresFiltering(self.CURRENT_INTERP_MOTION_DATA)
			else:
				print "need length of motion data > 8"
				return 0
			print "I get: ", banddata
			self.ui.addGainSliders(len(banddata[0]))
		except:
			print "multiresfilter() failed:"
			
	def resample(self):
		try:
			print "sampling..."
			resample = resampling.resample
			rate = self.ui.resampRateSpinBox.value()
			resampddata = [resample(data, rate) for data in self.CURRENT_INTERP_MOTION_DATA]
			#self.ms.multiresFiltering(new_data)
			#self.updatePlot()
			self.plotMotion(resampddata)
			self.updateCurrentInterpMotionData(resampddata)
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
	
	def runMotion(self):
		try:
			if self.CURRENT_INTERP_MOTION_DATA != []:
				motion = self.CURRENT_INTERP_MOTION_DATA
			else: motion = self.CURRENT_MOTION_DATA
						
			self.k1 = khr1Interface(self.khr1Device, motion)
			self.k1.start()
		except:
			print "runMotion() failed."		
		
	def updateInterpParams(self, value):
		callerID = str(self.sender().accessibleName())
		print "Param: %s" % (callerID)
		print "Old value: %f" % (self.interpParameters[callerID]),
		self.interpParameters[callerID] = value*.1
		print "New value: %f" % (self.interpParameters[callerID])	
		
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
		
	def loadNewMotion(self):
		motion = self.ui.motionComboBox.currentText()
		print "Load new motion..."
		print "New motion: %s" % (motion)
		self.ui.motionPlot.reInitialize()
		self.loadData(dataIndex=motion)
		self.CURRENT_INTERP_MOTION_DATA = []
		self.writeToStatusBar("Motion: %s loaded." % (motion))
		
		
	def loadMotionFiles(self):		
		return glob.glob(self.defaultMotionPath+"*.csv")   # <<< List of all motion files
		
	def formatMotionList(self, motionList):		
		pathname = re.compile('(\/home\/msunardi\/Documents\/thesis\-stuff\/KHR\-1\-motions)\/((\w*)(\D*)(\w*)).csv', re.IGNORECASE)
		for path in motionList:
			name = pathname.match(path).group(2)
			self.motionSignalPath[name] = path
			
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
