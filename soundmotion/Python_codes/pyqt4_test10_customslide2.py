

import sys
from PyQt4 import QtGui, QtCore


class SigSlot(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('signal & slot')

        #lcd = QtGui.QLCDNumber(self)
        self.lcd = QtGui.QDoubleSpinBox()
        self.lcd.setSingleStep(0.01)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.lcd)
        vbox.addWidget(self.slider)

        self.setLayout(vbox)
        self.connect(self.slider,  QtCore.SIGNAL('valueChanged(int)'), self.setSpinBoxValue )
        self.connect(self.lcd, QtCore.SIGNAL('valueChanged(double)'), self.setSliderPosition)
        self.resize(250, 150)

    def setSpinBoxValue(self):
        print "Set Spin from slider %d to %.12e\n" % (self.slider.value(), self.slider.value()*0.01)
        print "Current Spin value: %.17e\n" % self.lcd.value()
        print "Difference: %.15e\n" % (self.lcd.value() - self.slider.value()*0.01)
        self.lcd.setValue(self.slider.value()*0.01)

    def setSliderPosition(self):
        print "Set Slider from %.12e to %.12e\n" % (self.lcd.value(), self.lcd.value()*100)
        self.slider.setValue(self.lcd.value()*100)

app = QtGui.QApplication(sys.argv)
qb = SigSlot()
qb.show()
sys.exit(app.exec_())

