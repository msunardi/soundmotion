import sys
from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
from math import *
import numpy
from new_ui3_copy8 import Ui_MainWindow
from mosynth11_p import MotionSynthesizer
from KHR1interface2 import khr1Interface
import resampling

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.emote_parameters = {"weight": 0, "time": 0, "space": 0, "flow": 0}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setVariables()
        QtCore.QObject.connect(self.ui.weightSlider, QtCore.SIGNAL("valueChanged(int)"), self.weightChange)
        QtCore.QObject.connect(self.ui.timeSlider, QtCore.SIGNAL("valueChanged(int)"), self.timeChange)
        QtCore.QObject.connect(self.ui.spaceSlider, QtCore.SIGNAL("valueChanged(int)"), self.spaceChange)
        QtCore.QObject.connect(self.ui.flowSlider, QtCore.SIGNAL("valueChanged(int)"), self.flowChange)
        QtCore.QObject.connect(self.ui.expEdit, QtCore.SIGNAL("returnPressed()"), self.evaluateExp)
        QtCore.QObject.connect(self.ui.expButton, QtCore.SIGNAL("released()"), self.applyWaveshape)
        # === Apply action to the self.ui.runbutton
        QtCore.QObject.connect(self.ui.runbutton, QtCore.SIGNAL("released()"), self.runData)
        QtCore.QObject.connect(self.ui.run, QtCore.SIGNAL("triggered()"), self.runData)

        QtCore.QObject.connect(self.ui.resamplebutton, QtCore.SIGNAL("released()"), self.resampleData)
        QtCore.QObject.connect(self.ui.restorebutton, QtCore.SIGNAL("released()"), self.restoreData)
        self.connect(self.ui.exit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))

        self.loadData()            

        QtCore.QObject.connect(self.ui.pointSelector, QtCore.SIGNAL("currentIndexChanged(int)"), self.setPointSlider)
        QtCore.QObject.connect(self.ui.pointSlider, QtCore.SIGNAL("valueChanged(int)"), self.pointChange)
        QtCore.QObject.connect(self.ui.pointSlider, QtCore.SIGNAL("valueChanged(int)"), self.pointLineEditChange)
        QtCore.QObject.connect(self.ui.pointButton, QtCore.SIGNAL("released()"), self.applyWaveshape2)
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
            print self.bandAdjusters

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
        #self.tmpData = self.ms.DATA
        #self.ms.DATA = self.ms.interpolate(self.allData)
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

        # --- moved to function updatePlot()
        #for channel in range(self.channels):
        #    self.ui.qwtPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))
        self.updatePlot()
        
        print "Sender: %s, value: %f" % (self.sender().accessibleName(), self.sender().value()*0.1)#, self.tmpData[channel]
        #print "number of gains", type(self.ms.countGains())
        self.ms.DATA = self.ms.returnNewData()

        #self.ui.qwtPlot.changeCurve(channel, self.tmpData[])
        #pass
   
    def runData(self):
        khr1Interface("/dev/ttyUSB0", self.ms.DATA).start()
        #self.khr1.run(self.ms.returnNewData())
        #self.khr1.run(self.ms.returnNormalized())
        
    def resampleData(self):
        resample = resampling.resample
        rate = self.ui.rateSpinBox.value()
        new_data = []
        for data in self.ms.DATA:
            new_data.append(resample(data, rate))
        self.ms.multiresFiltering(new_data)
        #for channel in range(self.channels):
        #    self.ui.qwtPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))
        self.updatePlot()

    def restoreData(self):
        self.ms.multiresFiltering(self.newData)
        self.updatePlot()

    def updatePlot(self):
        for channel in range(self.channels):
            self.ui.qwtPlot.changeCurve(channel, self.ms.getNewSingleChannelData(channel))

    def loadData(self):
        # === Read data                                   
        #self.allData = self.ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/better_fwd_walk_data.csv")
        self.allData = self.ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
        #self.allData = self.ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/home.csv")

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

        # === Additional waveshaping data
        self.waveshape = numpy.zeros(len(self.newData))
        self.waveshapePoints = len(self.waveshape)/10 # <<< === careful!!!  if len is < 10..?
        #self.points = numpy.zeros(len(self.allData[0]))
        #self.new_points = self.ms.interpolate2(self.points)
        indexstring = []
        for i in range(len(self.allData[0])):
            indexstring.append(str(i))
        print indexstring
        self.ui.pointSelector.addItems(indexstring)
        self.plotWave(self.ui.wavePlot, range(len(self.waveshape)), self.waveshape)
        #self.plotWave(self.ui.wavePlot, range(len(self.new_points)), self.new_points)

        # --- These are the actual editable points
        self.points = numpy.zeros(len(self.allData[0]))
        self.new_points = self.ms.interpolate2(self.points)
        self.currentPointIndex = 0

        #self.ms.DATA = self.newData

# === WAVESHAPING

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
            #self.ms.DATA = self.y
        except:
            self.ui.statusbar.showMessage("%s is invalid!" % text)

        self.plotExp(self.ui.expPlot, range(len(currentData[0])), self.y)

# === WAVESHAPING 2

    def setPointSlider(self, index):
        """ Sets the value of the slider with the current index
        """
        self.currentPointIndex = index
        point = self.points[index] * 10
        position = int(point)
        self.ui.pointSlider.setSliderPosition(position)  # self.points is in float
        
        print "current point index is: ", self.currentPointIndex

    def pointLineEditChange(self, value):
        
        self.ui.pointLineEdit.setText(str(value * 0.1))
        
    def pointChange(self, value):
        self.points[self.currentPointIndex] = value * 0.1
        print "value in point ", self.currentPointIndex, "= ", self.points[self.currentPointIndex]
        print "points = ", self.points
        #a = []
        #a.append(self.points)
        self.new_points = self.ms.interpolate2(self.points)
        print "interpolated points: ", self.new_points
        self.plotWave(self.ui.wavePlot, range(len(self.new_points)), self.new_points)
        
    def plotWave(self, target, x, y):
        self.waveCurve = Qwt.QwtPlotCurve("waveCurve")
        self.waveCurve.setPen(Qt.QPen(Qt.Qt.red))
        self.waveCurve.setData(x, y)
        self.ui.wavePlot.clear()
        self.waveCurve.attach(target)
        self.ui.wavePlot.replot() 

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
            #data = self.ms.returnNewData()
            data = self.ms.DATA

            for i in range(len(data)):
                tmpData = list(numpy.add(data[i], numpy.multiply(data[i], numpy.multiply(self.y, self.ui.expSpinBox.value()))))
                tmp.append(tmpData)
                self.ui.qwtPlot.changeCurve(i, tmpData)

            #self.newData = tmp
            self.ms.DATA = tmp
                
        except:
            self.ui.statusbar.showMessage("Uh oh, something is wrong...")

    def applyWaveshape2(self):
        try:
            tmp = []
            #data = self.ms.returnNewData()
            data = self.ms.DATA
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
            


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
