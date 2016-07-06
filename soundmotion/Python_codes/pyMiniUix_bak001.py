# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MiniUI.ui'
#
# Created: Wed Sep  9 12:51:13 2009
#	  by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from plotter import MyPlot

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(657, 550)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.exit = QtGui.QAction(QtGui.QIcon('/usr/share/icons/Human/24x24/actions/exit.png'), 'Exit', MainWindow)
		self.exit.setShortcut('Ctrl+Q')
		self.exit.setStatusTip('Exit application')
		self.toolbar = MainWindow.addToolBar('Exit')
		self.toolbar.addAction(self.exit)
		self.gridLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
		self.gridLayoutWidget_2.setGeometry(QtCore.QRect(530, 0, 115, 251))
		self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
		self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
		self.gridLayout_2.setMargin(3)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.channelGroup = QtGui.QGroupBox(self.gridLayoutWidget_2)
		self.channelGroup.setObjectName("channelGroup")
		self.channelScrollArea = QtGui.QScrollArea(self.channelGroup)
		self.channelScrollArea.setGeometry(QtCore.QRect(10, 20, 91, 211))
		self.channelScrollArea.setFrameShape(QtGui.QFrame.WinPanel)
		self.channelScrollArea.setFrameShadow(QtGui.QFrame.Sunken)
		self.channelScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.channelScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.channelScrollArea.setWidgetResizable(False)
		self.channelScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.channelScrollArea.setObjectName("channelScrollArea")
		self.scrollAreaWidgetContents = QtGui.QWidget(self.channelScrollArea)
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 70, 100))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")		
		self.channelScrollArea.setWidget(self.scrollAreaWidgetContents)
		self.scrollAreaWidgetContents.scrollarea = self.channelScrollArea
		self.gridLayout_2.addWidget(self.channelGroup, 0, 0, 1, 1)
		self.gridLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
		self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 290, 191, 91))
		self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
		self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget_3)
		self.gridLayout_3.setMargin(3)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.motionFileGroup = QtGui.QGroupBox(self.gridLayoutWidget_3)
		self.motionFileGroup.setAlignment(QtCore.Qt.AlignCenter)
		self.motionFileGroup.setFlat(False)
		self.motionFileGroup.setCheckable(False)
		self.motionFileGroup.setObjectName("motionFileGroup")
		self.motionComboBox = QtGui.QComboBox(self.motionFileGroup)
		self.motionComboBox.setGeometry(QtCore.QRect(10, 20, 171, 25))
		self.motionComboBox.setObjectName("motionComboBox")
		self.motionLoadButton = QtGui.QPushButton(self.motionFileGroup)
		self.motionLoadButton.setGeometry(QtCore.QRect(50, 50, 91, 27))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.motionLoadButton.sizePolicy().hasHeightForWidth())
		self.motionLoadButton.setSizePolicy(sizePolicy)
		self.motionLoadButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
		font = QtGui.QFont()
		self.motionLoadButton.setFont(font)
		self.motionLoadButton.setCursor(QtCore.Qt.PointingHandCursor)
		self.motionLoadButton.setObjectName("motionLoadButton")
		self.gridLayout_3.addWidget(self.motionFileGroup, 1, 0, 1, 1)
		self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 511, 251))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setMargin(3)
		self.gridLayout.setObjectName("gridLayout")
		self.motionTabs = QtGui.QTabWidget(self.gridLayoutWidget)
		self.motionTabs.setObjectName("motionTabs")
		self.tab = QtGui.QWidget()
		self.tab.setObjectName("tab")
		
		self.motionPlot = MyPlot(self.tab)
		self.motionPlot.setGeometry(QtCore.QRect(10, 10, 470, 181))
		self.motionPlot.setObjectName("motionPlot")
		self.motionTabs.addTab(self.tab, "")
		#self.tab_2 = QtGui.QWidget()
		#self.tab_2.setObjectName("tab_2")
		#self.motionTabs.addTab(self.tab_2, "")
		self.gridLayout.addWidget(self.motionTabs, 0, 0, 1, 1)
		self.gridLayoutWidget_4 = QtGui.QWidget(self.centralwidget)
		self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 390, 191, 91))
		self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
		self.gridLayout_5 = QtGui.QGridLayout(self.gridLayoutWidget_4)
		self.gridLayout_5.setMargin(3)
		self.gridLayout_5.setObjectName("gridLayout_5")
		self.controlsGroup = QtGui.QGroupBox(self.gridLayoutWidget_4)
		self.controlsGroup.setObjectName("controlsGroup")
		self.motionPlayButton = QtGui.QToolButton(self.controlsGroup)
		self.motionPlayButton.setGeometry(QtCore.QRect(50, 20, 51, 22))
		self.motionPlayButton.setCursor(QtCore.Qt.PointingHandCursor)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("../../../usr/share/icons/gnome/24x24/actions/gtk-media-play-ltr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.motionPlayButton.setIcon(icon)
		self.motionPlayButton.setObjectName("motionPlayButton")
		self.motionResetButton = QtGui.QPushButton(self.controlsGroup)
		self.motionResetButton.setGeometry(QtCore.QRect(50, 50, 91, 27))
		self.motionResetButton.setCursor(QtCore.Qt.PointingHandCursor)
		self.motionResetButton.setObjectName("motionResetButton")
		self.motionStopButton = QtGui.QToolButton(self.controlsGroup)
		self.motionStopButton.setGeometry(QtCore.QRect(100, 20, 41, 22))
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("../../../usr/share/icons/gnome/24x24/actions/gtk-media-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.motionStopButton.setIcon(icon1)
		self.motionStopButton.setObjectName("motionStopButton")
		self.motionStopButton.setCursor(QtCore.Qt.PointingHandCursor)
		self.motionRewButton = QtGui.QToolButton(self.controlsGroup)
		self.motionRewButton.setGeometry(QtCore.QRect(20, 20, 31, 22))
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("../../../usr/share/icons/gnome/24x24/actions/media-seek-backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.motionRewButton.setIcon(icon2)
		self.motionRewButton.setObjectName("motionRewButtion")
		self.motionRewButton.setCursor(QtCore.Qt.PointingHandCursor)
		self.motionFwdButton = QtGui.QToolButton(self.controlsGroup)
		self.motionFwdButton.setGeometry(QtCore.QRect(140, 20, 31, 22))
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap("../../../usr/share/icons/gnome/24x24/actions/gtk-media-forward-ltr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.motionFwdButton.setIcon(icon3)
		self.motionFwdButton.setObjectName("motionFwdButton")
		self.motionFwdButton.setCursor(QtCore.Qt.PointingHandCursor)
		self.gridLayout_5.addWidget(self.controlsGroup, 0, 0, 1, 1)
		self.gridLayoutWidget_5 = QtGui.QWidget(self.centralwidget)
		self.gridLayoutWidget_5.setGeometry(QtCore.QRect(210, 290, 431, 191))
		self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
		self.gridLayout_6 = QtGui.QGridLayout(self.gridLayoutWidget_5)
		self.gridLayout_6.setMargin(3)
		self.gridLayout_6.setObjectName("gridLayout_6")
		self.motionToolTabs = QtGui.QTabWidget(self.gridLayoutWidget_5)
		self.motionToolTabs.setObjectName("motionToolTabs")
		self.tab_3 = QtGui.QWidget()
		self.tab_3.setObjectName("tab_3")
		self.motionToolTabs.addTab(self.tab_3, "")
		self.tab_4 = QtGui.QWidget()
		self.tab_4.setObjectName("tab_4")
		self.motionToolTabs.addTab(self.tab_4, "")
		self.gridLayout_6.addWidget(self.motionToolTabs, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 22))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		self.motionToolTabs.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	# Populating the list of channel/servo checkboxes  in the channelScrollArea
	def populateChannelList(self, numOfChannels=24, robot='KHR1'):
		self.channels = {}		# Store the check
		chDimX = 100
		chDimY = 30
				
		for i in range(numOfChannels):
			self.channels[str(i)] = QtGui.QCheckBox(self.scrollAreaWidgetContents)
			self.channels[str(i)].setText('ch'+str(i))
			self.channels[str(i)].setGeometry(QtCore.QRect(10, i*30, chDimX, chDimY))
			
			if robot == 'KHR1':			# The following setup is specific for KHR-1
				if i in [3,4,9,10,11,17,23]:
					self.channels[str(i)].setEnabled(False)		# Disable the unused channels/servos
				else:
					self.channels[str(i)].setEnabled(True)		# Enable all the used channels/servos
					self.channels[str(i)].setChecked(True)		# visible=True by default for all used channels/servos
		self.scrollAreaWidgetContents.adjustSize()	# Allow the scrollarea widget to automatically adjust its size to fit the contents
	
	def populateMotionBox(self, motionList, defaultIndex=None):
		self.motionComboBox.addItems(motionList)
		if defaultIndex is None:
			self.motionComboBox.setCurrentIndex(1)
		   #self.ui.comboBoxMotionSignal.setCurrentIndex(4)
		else:
			self.motionComboBox.setCurrentIndex(defaultIndex)
	
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MiniUI", None, QtGui.QApplication.UnicodeUTF8))
		self.channelGroup.setTitle(QtGui.QApplication.translate("MainWindow", "Channel visibility:", None, QtGui.QApplication.UnicodeUTF8))
		self.motionFileGroup.setTitle(QtGui.QApplication.translate("MainWindow", "Motion File:", None, QtGui.QApplication.UnicodeUTF8))
		self.motionLoadButton.setText(QtGui.QApplication.translate("MainWindow", "Load Motion", None, QtGui.QApplication.UnicodeUTF8))
		self.motionTabs.setTabText(self.motionTabs.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
		#self.motionTabs.setTabText(self.motionTabs.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))
		#self.controlsGroup.setTitle(QtGui.QApplication.translate("MainWindow", "Motion Controls:", None, QtGui.QApplication.UnicodeUTF8))
		self.motionPlayButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
		self.motionResetButton.setText(QtGui.QApplication.translate("MainWindow", "Reset Data", None, QtGui.QApplication.UnicodeUTF8))
		self.motionStopButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
		self.motionRewButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
		self.motionFwdButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
		self.motionToolTabs.setTabText(self.motionToolTabs.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
		self.motionToolTabs.setTabText(self.motionToolTabs.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4.Qwt5 import QwtPlot
