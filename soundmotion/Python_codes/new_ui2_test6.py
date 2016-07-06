import sys
from PyQt4 import QtCore, QtGui
from new_ui2_copy3 import Ui_MainWindow
from mosynth9_p import MotionSynthesizer

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.emote_parameters = {"weight": 0, "time": 0, "space": 0, "flow": 0}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setVariables()
        QtCore.QObject.connect(self.ui.Weight, QtCore.SIGNAL("valueChanged(int)"), self.weightChange)
        QtCore.QObject.connect(self.ui.Time, QtCore.SIGNAL("valueChanged(int)"), self.timeChange)
        QtCore.QObject.connect(self.ui.Space, QtCore.SIGNAL("valueChanged(int)"), self.spaceChange)
        QtCore.QObject.connect(self.ui.Flow, QtCore.SIGNAL("valueChanged(int)"), self.flowChange)

        self.loadData()


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

    def weightChange(self):
        self.ui.Text.setText(str(self.ui.Weight.value()))
        self.emote_parameters["weight"] = self.ui.Weight.value()
        self.ui.statusbar.showMessage("Weight value changed to "+ str(self.emote_parameters["weight"]))
        #self.ui.qwtPlot.changeCurve(0, range(0, 2*self.emote_parameters["weight"], 1))

    def timeChange(self):
        self.emote_parameters["time"] = self.ui.Time.value()
        self.ui.statusbar.showMessage("Time value changed to "+ str(self.emote_parameters["time"]))
        #self.ui.qwtPlot.changeCurve(1, range(0, 2*self.emote_parameters["weight"], 1))

    def spaceChange(self):
        self.emote_parameters["space"] = self.ui.Space.value()
        self.ui.statusbar.showMessage("Space value changed to "+ str(self.emote_parameters["space"]))
        #self.ui.addGainSliders(self.emote_parameters["weight"])
        #print type(self.ui.gainSliders[0])

    def flowChange(self):
        self.emote_parameters["flow"] = self.ui.Flow.value()
        self.ui.statusbar.showMessage("Flow value changed to "+ str(self.emote_parameters["flow"]))

    def applySignalSlot(self, how_many):
        self.ui.addGainSliders(how_many)
        print "gain sliders: "+str(how_many)
        #self.ssmapper = QtCore.QSignalMapper(self)
        #self.mapGains(how_many)
        #print "band adjusters: " + str(len(self.bandAdjusters))
        #print "band adjuster 0: " + str(type(self.bandAdjusters[0]))
        #print str(type(self.applySignalSlot))
        #index = 0

        #QtCore.QObject.connect(self.ui.gainSliders[1], QtCore.SIGNAL("valueChanged(int)"), self.adjustGain)

        for gs in self.ui.gainSliders:
            #print type(gs)
            #QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), self.ssmapper, QtCore.SLOT("map()"))
            #self.ssmapper.setMapping(gs, self.adjustGain(index))
            #QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), lambda x = index: self.adjustGain(x))
            QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), self.adjustGain)
            #index += 1
            #print str(index)
        
        #pass

    def mapGains(self, how_many):
        for i in range(how_many):
            self.bandAdjusters.append(self.adjustGain())
            print self.bandAdjusters

    def adjustGain(self, value):
        """new = self.ms.mrfDoItAll(self.newData, 0, 0, self.ui.gainSliders[0].value)
        for i in range(len(new)):
            self.ui.qwtPlot.changeCurve(i, new[i])
        self.ui.qwtPlot.plotCurves()        
        """
        # self.sender() -- hidden method, to identify which object just sent a signal
        print self.sender().accessibleName()

        #channel = 7
        gainIndex = int(self.sender().accessibleName())
        #mx = self.ms.mrfDoItAll(self.newData, channel, self.ms.countGains(), self.ui.gainSliders[1].value()*0.1)
        #mx = self.ms.mrfDoItAll(self.newData, channel, self.ms.countGains(), value*0.1)
        #print "channels: "+str(len(self.newData))

        # === modify the gains for the corresponding bands for all channels
        #for channel in range(self.channels)):
            #self.tmpData = self.ms.mrfDoItAll(self.newData, channel, gainIndex, value)
        self.tmpData = self.newData
        # === redraw 
        for i in range(self.ms.countGains()):
            for channel in range(self.channels):
                # === if it's not the changed slider...
                if i != gainIndex:
                
                    self.tmpData = self.ms.mrfDoItAll(self.tmpData, channel, i, self.ui.gainSliders[i].value())
                # === otherwise, it's the changed slider    
                else:
                    self.tmpData = self.ms.mrfDoItAll(self.tmpData, channel, gainIndex, value)

                # === 
                self.ui.qwtPlot.changeCurve(channel, self.tmpData[channel])
        
        print self.sender().value()#, self.tmpData[channel]
        #print "number of gains", type(self.ms.countGains())

        #self.ui.qwtPlot.changeCurve(channel, self.tmpData[])
        #pass
        

    def loadData(self):
        # === Read data                                   
        self.allData = self.ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
        self.ms.DATA = self.allData
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
        # === Apply interpolation
        self.newData = self.ms.interpolate(tmp)
        # === copy the data
        self.tmpData = self.newData

        # === global variable # of channels
        self.channels = len(self.newData)

        
        # === Add curves to plot
        for i in self.newData:
            self.ui.qwtPlot.addCurve(i)

        # === Get the bandpass filter bands
        self.freqBands = self.ms.multiresFiltering(self.allData)
        # === Create sliders for each bands
        self.applySignalSlot(len(self.freqBands[0]))
        print self.freqBands[0]


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
