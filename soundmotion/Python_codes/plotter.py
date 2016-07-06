import sys
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *

class MyPlot(Qwt.QwtPlot):
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)
        self.setAxisMaxMajor(Qwt.QwtPlot.xTop, 10)
        #self.setTitle('Aghh! Curves!')
        self.setTitle(' ')
        # set background to white
        self.setCanvasBackground(Qt.Qt.white)
        # set plot layout
        self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setAlignCanvasToScales(True)
        # attach grid
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        #grid.setPen(Qt.QPen(Qt.Qt.Black, 0, Qt.Qt.DotLine))
        self.colors = [Qt.Qt.black, Qt.Qt.blue, Qt.Qt.cyan, Qt.Qt.gray, Qt.Qt.green, Qt.Qt.magenta, Qt.Qt.red, Qt.Qt.yellow, Qt.Qt.darkBlue, Qt.Qt.darkCyan, Qt.Qt.darkGray, Qt.Qt.darkGreen, Qt.Qt.darkMagenta, Qt.Qt.darkRed, Qt.Qt.darkYellow]

        self.curves = []

    def reInitialize(self):
        self.detachItems()
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        #grid.setPen(Qt.QPen(Qt.Qt.Black, 0, Qt.Qt.DotLine))
        self.colors = [Qt.Qt.black, Qt.Qt.blue, Qt.Qt.cyan, Qt.Qt.gray, Qt.Qt.green, Qt.Qt.magenta, Qt.Qt.red, Qt.Qt.yellow, Qt.Qt.darkBlue, Qt.Qt.darkCyan, Qt.Qt.darkGray, Qt.Qt.darkGreen, Qt.Qt.darkMagenta, Qt.Qt.darkRed, Qt.Qt.darkYellow]

        self.curves = []

    def addCurve(self, new_curve_data):
        
        self.newcurve = Qwt.QwtPlotCurve("Ch"+str(len(self.curves)))
        self.newcurve.setData(arange(len(new_curve_data)), new_curve_data)
        self.curves.append(self.newcurve)
        self.newcurve.attach(self)
        self.plotCurves()
      
    def toggleVisible(self, curve_index, visible=None):
        if visible is not None:
            self.curves[curve_index].setVisible(visible)
        else:
            if self.curves[curve_index].isVisible():
                self.curves[curve_index].setVisible(False)
            else:
                self.curves[curve_index].setVisible(True)
                
        self.plotCurves()
		
	def curveIsVisible(self, curve_index):
		return self.curves[curve_index].isVisible()

    def changeCurve(self, curve_index, curve_data):
        self.curves[curve_index].setData(range(len(curve_data)), curve_data)
        #self.newcurve.setData(range(len(curve_data)), curve_data)
        self.plotCurves()
        #print "changecurve"
                         
    def plotCurves(self):
        for curve in self.curves:
            curve.detach()
        
        i = 0
        for curve in self.curves:
            curve.setPen(Qt.QPen(self.colors[i%len(self.colors)]))
            curve.attach(self)
            i += 1

        self.replot()


"""========================
    TESTING
   ========================
"""
"""app = Qt.QApplication([])
plot = MyPlot()
plot.addCurve([1,2,6,1,7,112,63,63,23,2,5])
plot.addCurve([5,2,5,5,23,5,12,5,5,62,32,1])
plot.toggleVisible(0)
plot.show()
app.exec_()
"""
