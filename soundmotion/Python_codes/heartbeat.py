#!/usr/bin/env python

# The Python version of Qwt-5.0.0/examples/data_plot

# for debugging, requires: python configure.py  --trace ...
if False:
    import sip
    sip.settracemask(0x3f)

import random
import sys

from PyQt4 import Qt, QtCore
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *


class DataPlot(Qwt.QwtPlot):

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.Qt.white)
        self.alignScales()

        # Initialize data
        self.x = arange(0.0, 20.1, 0.5)
        self.y = zeros(len(self.x), Float)
        self.y[19] = .1
        self.y[20] = -.23
        self.y[21] = .3
        self.y[22] = -.07
        

        #self.setTitle("A Moving QwtPlot Demonstration")
        #self.setTitle("Heartbeat Monitor")
        #self.setCanvasBackground(Qt.Qt.black)
        
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        #self.curveR = Qwt.QwtPlotCurve("Data Moving Right")
        self.curveR = Qwt.QwtPlotCurve()
        self.curveR.attach(self)
        

        #self.curveL.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,
        #                                Qt.QBrush(),
        #                                Qt.QPen(Qt.Qt.yellow),
        #                                Qt.QSize(7, 7)))

        self.curveR.setPen(Qt.QPen(Qt.Qt.green))
        

        mY = Qwt.QwtPlotMarker()
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.attach(self)

        #self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        #self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")
        self.enableAxis(0, False)
        self.enableAxis(1, False)
    
        #self.timerid = self.startTimer(20)
        self.phase = 0.0

    # __init__()

    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(
                    Qwt.QwtAbstractScaleDraw.Backbone, False)

    # alignScales()
    
    def timerEvent(self, e):
        if self.phase > pi - 0.0001:
            self.phase = 0.0

        # y moves from left to right:
        # shift y array right and assign new value y[0]
        tmp = self.y[0]
        self.y = concatenate((self.y[1:], self.y[:1]), 1)
        self.y[-1] = tmp
        #self.y[0] = sin(self.phase) * (-1.0 + 2.0*random.random())
		
        self.curveR.setData(self.x, self.y)
        

        self.replot()
        #self.phase += pi*0.02

    # timerEvent() 

# class DataPlot
"""
def make():
    demo = DataPlot()    
    demo.resize(300, 300)
    demo.show()
    return demo

# make()

def main(args): 
    app = Qt.QApplication(args)
    demo = make()
    timer = QtCore.QBasicTimer()    # <<< CREATE QBasicTimer object
    timer.start(30, demo)           # <<< START QBasicTimer(interval (ms), QObject)
    sys.exit(app.exec_())

# main()

# Admire
if __name__ == '__main__':
    main(sys.argv)

# Local Variables: ***
# mode: python ***
# End: ***

"""
