#!/usr/bin/env python
#
#       pyqt4_test11_scrollbar.py
#       
#       Copyright 2009 Mathias <msunardi@mbokjamu>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import sys
from PyQt4 import QtCore, QtGui

def main():
	app = QtGui.QApplication(sys.argv)
	sb = QtGui.QScrollBar()
	sb.setMinimum(0)
	sb.setMaximum(100)
	sb.connect(sb, QtCore.SIGNAL("sliderMoved(int)"), on_slider_moved)
	sb.show()
	app.exec_()
	
	return 0


def on_slider_moved(value): print "new slider position: %i" % (value, )

if __name__ == '__main__': main()
