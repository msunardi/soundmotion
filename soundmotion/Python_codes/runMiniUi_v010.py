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
		self.motionSignalPath = self.loadMotionFiles()
		
		self.ui.populateMotionBox(self.formatMotionList(self.motionSignalPath))		
		self.loadData(self.motionSignalPath[self.ui.motionComboBox.currentIndex()])
		
	def setVariables(self):
		self.motionSignalPath = []
		self.defaultMotionPath = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/"
		self.motionData = []
		self.ms = MotionSynthesizer()
		
	def setActions(self):
		print "setActions"
		for k,v in self.ui.channels.items():			
			QtCore.QObject.connect(v, QtCore.SIGNAL("stateChanged(int)"), self.toggleChannelVisible)
			
		QtCore.QObject.connect(self.ui.motionLoadButton, QtCore.SIGNAL("clicked()"), self.loadNewMotion)
			
	def toggleChannelVisible(self, value):
		ix = self.sender().accessibleName()		
		if value: value = True
		self.ui.motionPlot.toggleVisible(int(ix), value)
		
	def loadNewMotion(self):
		print "Load new motion..."
		print "New motion: %s" % (self.ui.motionComboBox.currentText())
		
	def loadMotionFiles(self):
		return glob.glob(self.defaultMotionPath+"*.csv")   # <<< List of all motion files
		
	def formatMotionList(self, motionList):		
		pathname = re.compile('(\/home\/msunardi\/Documents\/thesis\-stuff\/KHR\-1\-motions)\/((\w*)(\D*)(\w*)).csv', re.IGNORECASE)
		return [pathname.match(path).group(2) for path in motionList]
		
	def loadData(self, dataIndex=None):		
		try:
			# === Read data
			dataPath = self.motionSignalPath[self.ui.motionComboBox.currentIndex()]		# get path to motion file
			self.motionData = self.ms.read(dataPath)					# read motion file
			print "loadData(): motion data loaded."
			#self.ui.motionPlot.reInitialize()							# initialize plot object
			ch = 0
			
			for i in self.motionData:
				self.ui.motionPlot.addCurve(i) 							# plot each channel
				self.ui.motionPlot.toggleVisible(ch, self.ui.channels[str(ch)].isChecked()) # use this line when checkbox data is dictionary
				#self.ui.motionPlot.toggleVisible(ch, self.ui.channels[ch].isChecked())	# use this line when checkbox data is a list
				ch += 1
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
