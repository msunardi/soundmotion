import sys
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *


class XAxis(Qwt.QwtPlotItem):
    def __init__(self):
        Qwt.QwtPlotItem.__init__(self)
        self.obj = Qwt.QwtScaleDraw()
        self.setAxis(Qwt.QwtPlot.xBottom, Qwt.QwtPlot.yLeft)
        self.obj.setAlignment(Qwt.QwtScaleDraw.RightScale)
        self.obj2 = Qwt.QwtScaleDraw()
        self.obj2.setAlignment(Qwt.QwtScaleDraw.TopScale)


    def draw(self, painter, xMap, yMap, rect):
        # Drawing Y
        self.obj.move(round(xMap.xTransform(0.0)), yMap.p2())
        self.obj.setLength(yMap.p1()-yMap.p2())

        #Drawing X
        self.obj2.move(xMap.p1(), round(yMap.xTransform(0.0)))
        self.obj2.setLength(xMap.p2()-xMap.p1())
        
        self.obj.setScaleDiv(self.plot().axisScaleDiv(Qwt.QwtPlot.yRight))
        self.obj.draw(painter, self.plot().palette())

        self.obj2.setScaleDiv(self.plot().axisScaleDiv(Qwt.QwtPlot.yRight))
        self.obj2.draw(painter, self.plot().palette())




app = Qt.QApplication([])
plot = Qwt.QwtPlot()
xaxis = XAxis()
xaxis.attach(plot)
plot.enableAxis(Qwt.QwtPlot.xBottom, False)
plot.enableAxis(Qwt.QwtPlot.yLeft, False)
plot.resize(500,400)
plot.show()
app.exec_()
