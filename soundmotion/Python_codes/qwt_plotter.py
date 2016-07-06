import sys
from Qwt4.Qwt import *
from qt import *
from Numeric import *


class Demo (QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
#        QWidget.__init__(self, args)
        print "Plotok!"
        self.aplot = QwtPlot('Plot', self)
        self.ca = self.aplot.insertCurve('y')
        self.aplot.setAxisMaxMajor(QwtPlot.xBottom, 20)
        self.aplot.setCurvePen(self.ca, QPen(Qt.red))
        #self.aplot.setCurveData(ca, arange(0.0,500.0,0.01), arange(0.0,500.0,0.01))

    def resizeEvent(self, e):
        x = e.size().width()
        y = e.size().height()
        self.aplot.resize(x, y)
        self.aplot.move(0, 0)
        #self.lplot.resize(x, y)
        #self.lplot.move(0, y)

    def addData(self, data1, data2):
        self.curve1 = QwtPlotCurve('curve 1', self)
        self.curve2 = QwtPlotCurve('curve 2', self)
        self.curve1.setData(data1, arange(len(data1)))
        self.curve2.setData(data2, arange(len(data2)))
        

    def plotData(self, data):
        self.aplot.setCurveData(self.ca, arange(0, len(data), 1), data)
        self.aplot.replot()

"""app = QApplication(sys.argv)
demo = Demo()
app.setMainWidget(demo)
demo.resize(400,400)
demo.show()
app.exec_loop()
"""

