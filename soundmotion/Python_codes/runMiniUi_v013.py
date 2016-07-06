import sys, glob, re

import PyQt4.Qwt5 as Qwt
from PyQt4 import QtCore, QtGui, Qt
from pyMiniUix import Ui_MainWindow
from mosynth17_p import MotionSynthesizer

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
		self.motionPath = []
		self.motionSignalPath = {}
		self.defaultMotionPath = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/"
		self.CURRENT_MOTION_DATA = []
		self.ms = MotionSynthesizer()
		
		self.interpParameters = {'tension': 0, 'bias': 0, 'continuity': 0}
		
	def setActions(self):
		print "setActions"
		
		self.setActionsChannelsCheckBox()
		self.setActionsInterpolation()
		QtCore.QObject.connect(self.ui.motionLoadButton, QtCore.SIGNAL("clicked()"), self.loadNewMotion)
	
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
		
	def updateInterpParams(self, value):
		callerID = str(self.sender().accessibleName())
		print "Param: %s" % (callerID)
		print "Old value: %f" % (self.interpParameters[callerID]),
		self.interpParameters[callerID] = value*.1
		print "New value: %f" % (self.interpParameters[callerID])
	
	def setInterpTension(self, value):
		print "Old Tension =", self.interpParameters['tension'],
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
		
	def interpMotion(self):
		print "interpolating..."
	
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
		
	def loadData(self, dataIndex):		
		try:
			# === Read data
			#dataPath = self.motionSignalPath[self.ui.motionComboBox.currentIndex()]		# get path to motion file
			dataIndex = str(dataIndex)
			dataPath = self.motionSignalPath[dataIndex]		# get path to motion file
			motionData = self.ms.read(dataPath)					# read motion file
			print "loadData(): motion data loaded."
			#self.ui.motionPlot.reInitialize()							# initialize plot object
			ch = 0
			
			for i in motionData:
				self.ui.motionPlot.addCurve(i) 							# plot each channel
				self.ui.motionPlot.toggleVisible(ch, self.ui.channels[str(ch)].isChecked()) # use this line when checkbox data is dictionary
				#self.ui.motionPlot.toggleVisible(ch, self.ui.channels[ch].isChecked())	# use this line when checkbox data is a list
				ch += 1
			
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
