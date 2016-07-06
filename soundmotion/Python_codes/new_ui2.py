# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_ui2.ui'
#
# Created: Fri Jan 30 18:43:04 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.qwtPlot = QwtPlot(self.centralwidget)
        self.qwtPlot.setGeometry(QtCore.QRect(0, 30, 791, 261))
        self.qwtPlot.setObjectName("qwtPlot")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 300, 781, 241))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.Weight = QtGui.QSlider(self.tab)
        self.Weight.setGeometry(QtCore.QRect(20, 40, 16, 160))
        self.Weight.setOrientation(QtCore.Qt.Vertical)
        self.Weight.setObjectName("Weight")
        self.Time = QtGui.QSlider(self.tab)
        self.Time.setGeometry(QtCore.QRect(60, 40, 16, 160))
        self.Time.setOrientation(QtCore.Qt.Vertical)
        self.Time.setObjectName("Time")
        self.Space = QtGui.QSlider(self.tab)
        self.Space.setGeometry(QtCore.QRect(100, 40, 16, 160))
        self.Space.setOrientation(QtCore.Qt.Vertical)
        self.Space.setObjectName("Space")
        self.Flow = QtGui.QSlider(self.tab)
        self.Flow.setGeometry(QtCore.QRect(140, 40, 16, 160))
        self.Flow.setOrientation(QtCore.Qt.Vertical)
        self.Flow.setObjectName("Flow")
        self.verticalSlider_6 = QtGui.QSlider(self.tab)
        self.verticalSlider_6.setGeometry(QtCore.QRect(310, 40, 16, 160))
        self.verticalSlider_6.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_6.setObjectName("verticalSlider_6")
        self.verticalSlider_7 = QtGui.QSlider(self.tab)
        self.verticalSlider_7.setGeometry(QtCore.QRect(270, 40, 16, 160))
        self.verticalSlider_7.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_7.setObjectName("verticalSlider_7")
        self.verticalSlider_8 = QtGui.QSlider(self.tab)
        self.verticalSlider_8.setGeometry(QtCore.QRect(230, 40, 16, 160))
        self.verticalSlider_8.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_8.setObjectName("verticalSlider_8")
        self.verticalSlider_9 = QtGui.QSlider(self.tab)
        self.verticalSlider_9.setGeometry(QtCore.QRect(350, 40, 16, 160))
        self.verticalSlider_9.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_9.setObjectName("verticalSlider_9")
        self.Text = QtGui.QTextEdit(self.tab)
        self.Text.setGeometry(QtCore.QRect(510, 30, 104, 75))
        self.Text.setObjectName("Text")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "LMA Stuff", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Signalz", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4.Qwt5 import QwtPlot
