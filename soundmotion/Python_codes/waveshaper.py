import sys

from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from waveshapingui2 import Ui_MainWindow
from PyQt4.Qwt5.anynumpy import *

class waveshaper(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.x = arange(0, 200, 0.01)
        self.y = 0.02*self.x + 10
        self.ui.Knob.setValue(2)

        QtCore.QObject.connect(self.ui.Knob, QtCore.SIGNAL("valueChanged(double)"), self.adjustData1)
        QtCore.QObject.connect(self.ui.Knob_2, QtCore.SIGNAL("valueChanged(double)"), self.adjustData2)
        self.curve = Qwt.QwtPlotCurve("data")
        self.setData()

    def setData(self):
        
        self.curve.setData(self.x, self.y)
        self.curve.attach(self.ui.qwtPlot)
        self.ui.qwtPlot.replot()

    def adjustData1(self, value):
        #self.x = arange(-(value)*pi, value*pi, 0.01)
        self.y = 0.02*value*self.x + 10
        self.curve.detach()
        self.setData()
        self.ui.qwtPlot.refresh()

    def adjustData2(self, value):
        #self.x = arange(-(value)*pi, value*pi, 0.01)
        #self.y = 2*self.x + 10*value
        self.x = arange(0, 50*value, 0.01)
        self.curve.detach()
        self.setData()
        self.ui.qwtPlot.refresh()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = waveshaper()
    myapp.show()
    sys.exit(app.exec_())
