import sys
from Qwt4.Qwt import *
from qt import *
from Numeric import *

class Demo (QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        self.aplot = QwtPlot('Plot', self)
        ca = self.aplot.insertCurve('y')
        self.aplot.setCurvePen(ca, QPen(Qt.red))
        self.aplot.setCurveData(ca, arange(0.0,500.0,0.01), arange(0.0,500.0,0.01))

    def resizeEvent(self, e):
        x = e.size().width()
        #y = e.size().height()/2
        y = e.size().height()
        self.aplot.resize(x, y)
        self.aplot.move(0, 0)
        #self.lplot.resize(x, y)
        #self.lplot.move(0, y)

"""app = QApplication(sys.argv)
demo = Demo()
app.setMainWidget(demo)
demo.resize(400,400)
demo.show()
app.exec_loop()
"""

