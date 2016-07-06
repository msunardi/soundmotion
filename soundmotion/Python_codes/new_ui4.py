# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_ui3.ui'
#
# Created: Tue Feb  3 14:36:28 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from plotter import MyPlot
import KHR1_motionrange2 as khr1

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 650)

        self.gainLabels = []
        self.gainLineEdits = []
        self.gainSliders = []
        self.bodyStartSpinBoxes = []
        self.bodyEndSpinBoxes = []
        self.bodyLabels =[]
        
        #=== CREATE MAIN WINDOW ===
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #=== CREATE MAIN TAB WIDGET ===
        self.mainTabWidget = QtGui.QTabWidget(self.centralwidget)
        self.mainTabWidget.setGeometry(QtCore.QRect(0, 0, 800, 580))
        self.mainTabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.mainTabWidget.setObjectName("mainTabWidget")

        #=== CREATE THE FIRST TAB OF MAINTABWIDGET (MAIN UI)
        self.mainTab_0 = QtGui.QWidget()
        self.mainTab_0.setObjectName("mainTab_0")
        #=== CONTENT OF THE FIRST MAIN TAB:

        self.mainTabWidget.addTab(self.mainTab_0, "")   # Add the first main tab to the mainTabWidget
 
        #=== CREATE THE SECOND TAB OF MAINTABWIDGET (BACKEND UI)
        self.mainTab_1 = QtGui.QWidget()
        self.mainTab_1.setObjectName("mainTab_1")

        #=== CONTENTS OF THE SECOND MAIN TAB:
        ##=== FIRST CONTENT: QWT PLOTTER
        #self.qwtPlot = MyPlot(self.centralwidget)
        self.qwtPlot = MyPlot(self.mainTab_1)
        self.qwtPlot.setGeometry(QtCore.QRect(0, 30, 791, 261))
        self.qwtPlot.setObjectName("qwtPlot")

        ##=== SECOND CONTENT: TAB WIDGET
        #self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget = QtGui.QTabWidget(self.mainTab_1)
        self.tabWidget.setGeometry(QtCore.QRect(10, 300, 781, 251))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        ###=== CREATE FIRST TAB FOR THE BACKEND UI
        self.tab_0 = QtGui.QWidget()
        self.tab_0.setObjectName("tab_0")
        ####=== CONTENTS OF FIRST TAB OF BACKEND UI:
        #####=== BODY PARAMETERS FRAME (Contents will be created dynamically)
        self.bodyFrame = QtGui.QFrame(self.tab_0)
        self.bodyFrame.setGeometry(QtCore.QRect(10, 10, 765, 201))
        self.bodyFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bodyFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.bodyFrame.setLineWidth(3)
        self.bodyFrame.setObjectName("bodyFrame")
        self.tabWidget.addTab(self.tab_0, "")    # Add the first tab to the backend UI tabWidget
        
        ###=== CREATE SECOND TAB FOR THE BACKEND UI
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")        
        ####=== CONTENTS OF THE SECOND TAB OF BACKEND UI:
        #####=== FIRST FRAME: EFFORT PARAMETERS FRAME
        self.effortFrame = QtGui.QFrame(self.tab)
        self.effortFrame.setGeometry(QtCore.QRect(10, 10, 241, 201))
        self.effortFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.effortFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.effortFrame.setLineWidth(3)

        #####=== FIRST CONTENT IN FRAME: EFFORT PARAMETERS SLIDERS
        self.effortFrame.setObjectName("effortFrame")
        self.weightSlider = QtGui.QSlider(self.effortFrame)
        self.weightSlider.setGeometry(QtCore.QRect(20, 90, 20, 101))
        self.weightSlider.setOrientation(QtCore.Qt.Vertical)
        self.weightSlider.setObjectName("weightSlider")
        self.weightSlider.setMaximum(10)
        self.weightSlider.setMinimum(-10)
        self.weightSlider.setSliderPosition(0)
        self.timeSlider = QtGui.QSlider(self.effortFrame)
        self.timeSlider.setGeometry(QtCore.QRect(80, 90, 20, 101))
        self.timeSlider.setOrientation(QtCore.Qt.Vertical)
        self.timeSlider.setObjectName("timeSlider")
        self.timeSlider.setMaximum(10)
        self.timeSlider.setMinimum(-10)
        self.timeSlider.setSliderPosition(0)
        self.spaceSlider = QtGui.QSlider(self.effortFrame)
        self.spaceSlider.setGeometry(QtCore.QRect(140, 90, 20, 101))
        self.spaceSlider.setOrientation(QtCore.Qt.Vertical)
        self.spaceSlider.setObjectName("spaceSlider")
        self.spaceSlider.setMaximum(10)
        self.spaceSlider.setMinimum(-10)
        self.spaceSlider.setSliderPosition(0)
        self.flowSlider = QtGui.QSlider(self.effortFrame)
        self.flowSlider.setGeometry(QtCore.QRect(200, 90, 20, 101))
        self.flowSlider.setOrientation(QtCore.Qt.Vertical)
        self.flowSlider.setObjectName("flowSlider")
        self.flowSlider.setMaximum(10)
        self.flowSlider.setMinimum(-10)
        self.flowSlider.setSliderPosition(0)

        #####=== SECOND CONTENT IN FRAME: EFFORT PARAMETERS LINEEDITS & LABELS
        self.weightLineEdit = QtGui.QLineEdit(self.effortFrame)
        self.weightLineEdit.setGeometry(QtCore.QRect(10, 50, 41, 28))
        self.weightLineEdit.setObjectName("weightLineEdit")
        self.weightLineEdit.setText("0")
        self.timeLineEdit = QtGui.QLineEdit(self.effortFrame)
        self.timeLineEdit.setGeometry(QtCore.QRect(70, 50, 41, 28))
        self.timeLineEdit.setObjectName("timeLineEdit")
        self.timeLineEdit.setText("0")
        self.spaceLineEdit = QtGui.QLineEdit(self.effortFrame)
        self.spaceLineEdit.setGeometry(QtCore.QRect(130, 50, 41, 28))
        self.spaceLineEdit.setObjectName("spaceLineEdit")
        self.spaceLineEdit.setText("0")
        self.flowLineEdit = QtGui.QLineEdit(self.effortFrame)
        self.flowLineEdit.setGeometry(QtCore.QRect(190, 50, 41, 28))
        self.flowLineEdit.setObjectName("flowLineEdit")
        self.flowLineEdit.setText("0")
        self.weightLabel = QtGui.QLabel(self.effortFrame)
        self.weightLabel.setGeometry(QtCore.QRect(0, 30, 54, 18))
        self.weightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.weightLabel.setObjectName("weightLabel")
        self.timeLabel = QtGui.QLabel(self.effortFrame)
        self.timeLabel.setGeometry(QtCore.QRect(60, 30, 54, 18))
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.spaceLabel = QtGui.QLabel(self.effortFrame)
        self.spaceLabel.setGeometry(QtCore.QRect(120, 30, 54, 18))
        self.spaceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.spaceLabel.setObjectName("spaceLabel")
        self.flowLabel = QtGui.QLabel(self.effortFrame)
        self.flowLabel.setGeometry(QtCore.QRect(180, 30, 54, 18))
        self.flowLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.flowLabel.setObjectName("flowLabel")
        self.effortLabel = QtGui.QLabel(self.effortFrame)
        self.effortLabel.setGeometry(QtCore.QRect(10, 0, 111, 18))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.effortLabel.setFont(font)
        self.effortLabel.setObjectName("effortLabel")

        #####=== SECOND FRAME: SHAPE PARAMETERS FRAME
        self.shapeFrame = QtGui.QFrame(self.tab)
        self.shapeFrame.setGeometry(QtCore.QRect(260, 10, 261, 201))
        self.shapeFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.shapeFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.shapeFrame.setLineWidth(3)
        self.shapeFrame.setObjectName("shapeFrame")

        #####=== FIRST CONTENT IN SHAPE PARAMETERS FRAME: SHAPE PARAMETERS LINEEDITS & LABELS
        self.risesinkLineEdit = QtGui.QLineEdit(self.shapeFrame)
        self.risesinkLineEdit.setGeometry(QtCore.QRect(20, 50, 41, 28))
        self.risesinkLineEdit.setObjectName("risesinkLineEdit")
        self.opencloseLineEdit = QtGui.QLineEdit(self.shapeFrame)
        self.opencloseLineEdit.setGeometry(QtCore.QRect(140, 50, 41, 28))
        self.opencloseLineEdit.setObjectName("opencloseLineEdit")
        self.growshrinkLineEdit = QtGui.QLineEdit(self.shapeFrame)
        self.growshrinkLineEdit.setGeometry(QtCore.QRect(200, 50, 41, 28))
        self.growshrinkLineEdit.setObjectName("growshrinkLineEdit")
        self.advanceretreatLineEdit = QtGui.QLineEdit(self.shapeFrame)
        self.advanceretreatLineEdit.setGeometry(QtCore.QRect(80, 50, 41, 28))
        self.advanceretreatLineEdit.setObjectName("advanceretreatLineEdit")        
        self.risesinkLabel = QtGui.QLabel(self.shapeFrame)
        self.risesinkLabel.setGeometry(QtCore.QRect(10, 30, 54, 18))
        self.risesinkLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.risesinkLabel.setObjectName("risesinkLabel")
        self.advanceretreatLabel = QtGui.QLabel(self.shapeFrame)
        self.advanceretreatLabel.setGeometry(QtCore.QRect(70, 30, 54, 18))
        self.advanceretreatLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.advanceretreatLabel.setObjectName("advanceretreatLabel")
        self.opencloseLabel = QtGui.QLabel(self.shapeFrame)
        self.opencloseLabel.setGeometry(QtCore.QRect(130, 30, 54, 18))
        self.opencloseLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.opencloseLabel.setObjectName("opencloseLabel")
        self.growshrinkLabel = QtGui.QLabel(self.shapeFrame)
        self.growshrinkLabel.setGeometry(QtCore.QRect(190, 30, 54, 18))
        self.growshrinkLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.growshrinkLabel.setObjectName("growshrinkLabel")
        self.shapeLabel = QtGui.QLabel(self.shapeFrame)
        self.shapeLabel.setGeometry(QtCore.QRect(10, 0, 111, 18))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.shapeLabel.setFont(font)
        self.shapeLabel.setObjectName("shapeLabel")

        #####=== SECOND CONTENT IN SHAPE PARAMETERS FRAME: SHAPE PARAMETERS SLIDERS
        self.opencloseSlider = QtGui.QSlider(self.shapeFrame)
        self.opencloseSlider.setGeometry(QtCore.QRect(150, 90, 20, 101))
        self.opencloseSlider.setOrientation(QtCore.Qt.Vertical)
        self.opencloseSlider.setObjectName("opencloseSlider")
        self.opencloseSlider.setMaximum(5)
        self.opencloseSlider.setMinimum(-5)
        self.opencloseSlider.setSliderPosition(0)
        self.risesinkSlider = QtGui.QSlider(self.shapeFrame)
        self.risesinkSlider.setGeometry(QtCore.QRect(30, 90, 20, 101))
        self.risesinkSlider.setOrientation(QtCore.Qt.Vertical)
        self.risesinkSlider.setObjectName("risesinkSlider")
        self.risesinkSlider.setMaximum(5)
        self.risesinkSlider.setMinimum(-5)
        self.risesinkSlider.setSliderPosition(0)
        self.advanceretreatSlider = QtGui.QSlider(self.shapeFrame)
        self.advanceretreatSlider.setGeometry(QtCore.QRect(90, 90, 20, 101))
        self.advanceretreatSlider.setOrientation(QtCore.Qt.Vertical)
        self.advanceretreatSlider.setObjectName("advanceretreatSlider")
        self.advanceretreatSlider.setMaximum(5)
        self.advanceretreatSlider.setMinimum(-5)
        self.advanceretreatSlider.setSliderPosition(0)
        self.growshrinkSlider = QtGui.QSlider(self.shapeFrame)
        self.growshrinkSlider.setGeometry(QtCore.QRect(210, 90, 20, 101))
        self.growshrinkSlider.setOrientation(QtCore.Qt.Vertical)
        self.growshrinkSlider.setObjectName("growshrinkSlider")
        self.growshrinkSlider.setMaximum(5)
        self.growshrinkSlider.setMinimum(-5)
        self.growshrinkSlider.setSliderPosition(0)
        
        self.tabWidget.addTab(self.tab, "")    # Add second tab to the tabWidget

        ###=== CREATE THIRD TAB FOR BACKEND UI
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        ####=== FIRST CONTENT OF THIRD TAB OF BACKEND UI: FRAME FOR GAINS (Gain sliders are added dynamically)
        self.gainframe = QtGui.QFrame(self.tab_2) 
        self.gainFrame = QtGui.QFrame(self.tab_2)
        self.gainFrame.setGeometry(QtCore.QRect(10, 10, 700, 201))
        self.gainFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.gainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.gainFrame.setObjectName("gainframe")

        #=== Label for the Effort Parameters frame
        #self.effortLabel = QtGui.QLabel(self.effortFrame)
        self.effortLabel.setGeometry(QtCore.QRect(10, 0, 111, 18))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.effortLabel.setFont(font)
        self.effortLabel.setObjectName("effortLabel")

        #=== Label for the Gains frame
        self.gainLabel = QtGui.QLabel(self.gainFrame)
        self.gainLabel.setGeometry(QtCore.QRect(10, 0, 111, 18))
        gfont = QtGui.QFont()
        gfont.setWeight(75)
        gfont.setBold(True)
        self.gainLabel.setFont(gfont)
        self.gainLabel.setObjectName("gainLabel")
        self.tabWidget.addTab(self.tab_2, "")   # Add the third tab to the tabWidget
        
        #=== CREATE THE FOURTH TAB FOR BACKEND UI
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        ##=== CONTENT OF FOURTH TAB OF BACKEND UI: WAVESHAPING UI
        self.expLabel = QtGui.QLabel(self.tab_3)
        self.expLabel.setGeometry(QtCore.QRect(10, 10, 200, 25))
        self.expEdit = QtGui.QLineEdit(self.tab_3)
        self.expEdit.setGeometry(QtCore.QRect(210, 10, 200, 25))
        self.expSpinBox = QtGui.QDoubleSpinBox(self.tab_3)
        self.expXLabel = QtGui.QLabel(self.tab_3)
        self.expXLabel.setGeometry(QtCore.QRect(415, 10, 10, 25))
        self.expSpinBox.setGeometry(QtCore.QRect(430, 10, 50, 25))
        self.expSpinBox.setMaximum(2.00)
        self.expSpinBox.setMinimum(0.00)
        self.expSpinBox.setSingleStep(0.01)
        self.expSpinBox.setValue(1.00)
        self.expButton = QtGui.QPushButton(self.tab_3)
        self.expButton.setGeometry(QtCore.QRect(500,10, 50, 25))        
        self.expPlot = QwtPlot(self.tab_3)
        self.expPlot.setGeometry(QtCore.QRect(10, 50, 500, 150))
        self.tabWidget.addTab(self.tab_3, "")    # Add the fourth tab to the tabWidget

        self.mainTabWidget.addTab(self.mainTab_1, "")   # Add the first main tab to the mainTabWidget
 
        #=== Create toolbar buttons:
        #--- First button: Exit/Quit
        self.exit = QtGui.QAction(QtGui.QIcon('/usr/share/icons/Human/24x24/actions/exit.png'), 'Exit', MainWindow)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')

        #--- Second button: Run/Execute motion
        self.run = QtGui.QAction(QtGui.QIcon('/usr/share/icons/Human/24x24/actions/start.png'), 'Run', MainWindow)
        self.run.setShortcut('Ctrl+R')
        self.run.setStatusTip('Send to output')
        
        #=== Create the toolbar
        self.toolbar = MainWindow.addToolBar('Exit')
        self.toolbar.addAction(self.exit)
        self.toolbar = MainWindow.addToolBar('Execute')
        self.toolbar.addAction(self.run)
        MainWindow.setCentralWidget(self.centralwidget)
        #self.menubar = QtGui.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        #self.menubar.setObjectName("menubar")
        #MainWindow.setMenuBar(self.menubar)
        #self.toolbar = MainWindow.addToolBar("main")
        #self.toolbar.setObjectName("toolbar")
        #self.toolbar.addAction(self.bye())

        #--- create a Run button
        #self.runbutton = QtGui.QPushButton(MainWindow)
        self.runbutton = QtGui.QPushButton(self.mainTab_1)
        self.runbutton.setGeometry(QtCore.QRect(10, 10, 50, 30))
        self.runbutton.setObjectName("runbutton")

        #=== Setup the statusbar
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow UI v3", None, QtGui.QApplication.UnicodeUTF8))
        self.weightLabel.setText(QtGui.QApplication.translate("MainWindow", "Weight", None, QtGui.QApplication.UnicodeUTF8))
        self.timeLabel.setText(QtGui.QApplication.translate("MainWindow", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.spaceLabel.setText(QtGui.QApplication.translate("MainWindow", "Space", None, QtGui.QApplication.UnicodeUTF8))
        self.flowLabel.setText(QtGui.QApplication.translate("MainWindow", "Flow", None, QtGui.QApplication.UnicodeUTF8))
        self.effortLabel.setText(QtGui.QApplication.translate("MainWindow", "Effort Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.risesinkLabel.setText(QtGui.QApplication.translate("MainWindow", "Rise/Sink", None, QtGui.QApplication.UnicodeUTF8))
        self.advanceretreatLabel.setText(QtGui.QApplication.translate("MainWindow", "Adv/Ret", None, QtGui.QApplication.UnicodeUTF8))
        self.growshrinkLabel.setText(QtGui.QApplication.translate("MainWindow", "Gr/Sh", None, QtGui.QApplication.UnicodeUTF8))
        self.shapeLabel.setText(QtGui.QApplication.translate("MainWindow", "Shape Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.opencloseLabel.setText(QtGui.QApplication.translate("MainWindow", "Op/Cl", None, QtGui.QApplication.UnicodeUTF8))
        self.gainLabel.setText(QtGui.QApplication.translate("MainWindow", "Gains", None, QtGui.QApplication.UnicodeUTF8))
        self.expLabel.setText(QtGui.QApplication.translate("MainWindow", "Enter waveshaping function (in x): ", None, QtGui.QApplication.UnicodeUTF8))
        self.expXLabel.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.expButton.setText(QtGui.QApplication.translate("MainWindow", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.runbutton.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), QtGui.QApplication.translate("MainWindow", "LMA-Body", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "LMA-Effort/Shape", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Signals", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Waveshaping", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.mainTab_0), QtGui.QApplication.translate("MainWindow", "Main UI", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.mainTab_1), QtGui.QApplication.translate("MainWindow", "Behind the Scenes", None, QtGui.QApplication.UnicodeUTF8))



    def addGainSliders(self, how_many):
        
        for i in range(how_many):
            #=== Create labels for each gain
            self.gainLabels.append(QtGui.QLabel)
            self.gainLabels[i] = QtGui.QLabel(self.gainFrame)
            self.gainLabels[i].setGeometry(QtCore.QRect(i*60, 30, 54, 18))
            self.gainLabels[i].setAlignment(QtCore.Qt.AlignCenter)
            self.gainLabels[i].setObjectName("band"+str(i))
            self.gainLabels[i].setText("Band "+str(i))            

            #=== Create sliders for each gain
            self.gainSliders.append(QtGui.QSlider(self.gainFrame))
            self.gainSliders[i].setGeometry(QtCore.QRect(20 + i*60 , 90, 20, 101))
            self.gainSliders[i].setAccessibleName(str(i))
            self.gainSliders[i].setMaximum(50)
            self.gainSliders[i].setMinimum(-50)
            self.gainSliders[i].setSliderPosition(10)

            #=== Create Line Edit objects for each gain
            self.gainLineEdits.append(QtGui.QLineEdit)
            self.gainLineEdits[i] = QtGui.QLineEdit(self.gainFrame)
            self.gainLineEdits[i].setGeometry(QtCore.QRect(10 + i*60, 50, 41, 28))
            self.gainLineEdits[i].setObjectName("weightLineEdit")
            self.gainLineEdits[i].setText(str(self.gainSliders[i].value()*0.1))
            self.gainLineEdits[i].setAccessibleName(str(i))

            #>>NOT WORKING...self.gainframe.repaint(QtCore.QRect(10, 10, how_many*150, 201))       
            
        #length = len(self.gainSliders)-1
        #self.gainSliders[length].setGeometry(QtCore.QRect(20 + length*40 , 40, 16, 160))
        #pass

    def addBodySpinBoxes(self, data):
        how_many = len(data)
        data_length = len(data[0])
        x = 10
        for i in range(how_many):
            #=== Create labels for each channel
            self.bodyLabels.append(QtGui.QLabel)
            self.bodyLabels[i] = QtGui.QLabel(self.bodyFrame)
            self.bodyLabels[i].setGeometry(QtCore.QRect(x, 10 + (i%6)*30, 80, 25))
            self.bodyLabels[i].setObjectName("channel"+str(i))
            #self.bodyLabels[i].setText("Ch "+str(i))
            self.bodyLabels[i].setText(khr1.KHR1motionrange2[i][0])
            self.bodyLabels[i].setAccessibleName(str(i))            

            self.bodyStartSpinBoxes.append(QtGui.QSpinBox)
            self.bodyStartSpinBoxes[i] = QtGui.QSpinBox(self.bodyFrame)
            self.bodyStartSpinBoxes[i].setGeometry(QtCore.QRect(x + 75, 10+(i%6)*30, 50, 25))
            #self.bodyStartSpinBoxes[i].setObjectName("channel"+str(i)+"start")
            self.bodyStartSpinBoxes[i].setObjectName(khr1.KHR1motionrange2[i][0])            
            #self.bodyStartSpinBoxes[i].setMinimum(khr1.KHR1motionrange2[i][1])
            #self.bodyStartSpinBoxes[i].setMaximum(khr1.KHR1motionrange2[i][2])            
            #self.bodyStartSpinBoxes[i].setValue(data[i][0])
            self.bodyStartSpinBoxes[i].setMinimum(0)
            self.bodyStartSpinBoxes[i].setMaximum(data_length) 
            self.bodyStartSpinBoxes[i].setValue(0)            
            self.bodyStartSpinBoxes[i].setAccessibleName(str(i))

            self.bodyEndSpinBoxes.append(QtGui.QSpinBox)
            self.bodyEndSpinBoxes[i] = QtGui.QSpinBox(self.bodyFrame)
            self.bodyEndSpinBoxes[i].setGeometry(QtCore.QRect(x + 128, 10+(i%6)*30, 50, 25))
            #self.bodyEndSpinBoxes[i].setObjectName("channel"+str(i)+"end")
            self.bodyEndSpinBoxes[i].setObjectName(khr1.KHR1motionrange2[i][0])            
            #self.bodyEndSpinBoxes[i].setMinimum(khr1.KHR1motionrange2[i][1])
            #self.bodyEndSpinBoxes[i].setMaximum(khr1.KHR1motionrange2[i][2])
            #self.bodyEndSpinBoxes[i].setValue(data[i][data_length-1])
            self.bodyEndSpinBoxes[i].setMinimum(0)
            self.bodyEndSpinBoxes[i].setMaximum(data_length)
            self.bodyEndSpinBoxes[i].setValue(data_length)
            self.bodyEndSpinBoxes[i].setAccessibleName(str(i))  

            if i > 0 and i%6 == 5:
                x = x+190
                    

            
    def bye(self):
        print "Bye"

from PyQt4.Qwt5 import QwtPlot
