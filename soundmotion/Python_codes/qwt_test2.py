#From: http://svn.pardus.org.tr/projeler/pythonkitabi/ingilizce/appendices/qwt.sgml

import sys

from qt import *
from Qwt4.Qwt import *
from Numeric import *

def drange(start, stop, step):
    start, stop, step = float(start), float(stop), float(step)
    size = int(round((stop-start)/step))
    result = [start]*size
    for i in xrange(size):
        result[i] += i*step
    return result
        
def lorentzian(x):
    return 1.0/(1.0+(x-5.0)**2)


class ListArrayDemo(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        
        # create a plot widget for NumPy arrays
        self.aplot = QwtPlot('Plot -- NumPy arrays', self)
        # calculate 2 NumPy arrays
        xa = arange(0.0, 10.0, 0.01)
        ya = lorentzian(xa)
        # insert a curve, make it red and copy the arrays
        ca = self.aplot.insertCurve('y = lorentzian(x)')
        self.aplot.setCurvePen(ca, QPen(Qt.red))
        self.aplot.setCurveData(ca, xa, ya)

        # create a plot widget for lists of Python floats
        self.lplot = QwtPlot('Plot -- List of Python floats', self)
        # calculate 2 lists of Python floats
        xl = drange(0.0, 10.0, 0.01)
        yl = map(lorentzian, xl)
        # insert a curve, make it blue and copy the lists
        cl = self.lplot.insertCurve('y = lorentzian(x)')
        self.lplot.setCurvePen(cl, QPen(Qt.blue))
        self.lplot.setCurveData(cl, xl, yl)

    def resizeEvent(self, e):
        x = e.size().width()
        y = e.size().height()/2
        self.aplot.resize(x, y)
        self.aplot.move(0, 0)
        self.lplot.resize(x, y)
        self.lplot.move(0, y)

# admire	
app = QApplication(sys.argv)
demo = ListArrayDemo()
app.setMainWidget(demo)
demo.resize(400, 600)
demo.show()
app.exec_loop()
