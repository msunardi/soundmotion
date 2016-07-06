import sys
from PyQt4 import QtCore, QtGui
from new_ui2_copy2 import Ui_MainWindow
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
        self.ssmapper = QtCore.QSignalMapper(self)
        self.mapGains(how_many)
        print "band adjusters: " + str(len(self.bandAdjusters))
        print "band adjuster 0: " + str(type(self.bandAdjusters[0]))
        print str(type(self.applySignalSlot))
        index = 0
        
        for gs in self.ui.gainSliders:
            #print type(gs)
            QtCore.QObject.connect(gs, QtCore.SIGNAL("valueChanged(int)"), self.ssmapper, QtCore.SLOT("map()"))
            self.ssmapper.setMapping(gs, self.adjustGain(index))
            index += 1
            print str(index)
        
        #pass

    def mapGains(self, how_many):
        for i in range(how_many):
            self.bandAdjusters.append(self.adjustGain(i))
            print self.bandAdjusters

    def adjustGain(self, index, value=0):
        new = self.ms.mrfDoItAll(self.newData, 0, index, value)
        for i in range(len(new)):
            self.ui.qwtPlot.changeCurve(i, new[i])
        self.ui.qwtPlot.plotCurves()
                           
        #pass
        

    def loadData(self):
        # === Read data                                   
        self.allData = self.ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/better_fwd_walk_data.csv")
        print "Data loaded"

        # === Apply filter
        tmp = self.ms.mrfDoItAll(self.allData)
        # === Apply interpolation
        self.newData = self.ms.interpolate(tmp)
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
