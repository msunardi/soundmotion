#!/usr/bin/env python
#
#       py_test41_FusionCmd.py
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

sys.path.append("/home/msunardi/experimental4/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")

import KHR1Serial_test as KHR1Serial
import KHR1CmdBase as KHR1Cmd
import PyDebug
import threading, time


def main():
	print "Hello Python!"
	k = KHR1Cmd.KHR1CmdBase(port="/dev/ttyUSB0")
	print "Number of boards: %d" % (k.AttrHasNumOfBoards())
	poslist = k.CmdGetCurPos()
	print "Current position:", poslist
	poslist[5] = 0
	print k.CmdSetCurPos(3, poslist)
	poslist[5] = 180	
	#time.sleep(.3)
	
	print k.CmdSetCurPos(4, poslist)
	while k.CmdGetCurPos() != poslist:
		print "x"
		print KHR1Serial.ACK
	poslist[5] = 0
	#time.sleep(.3)
	
	print k.CmdSetCurPos(5, poslist)
	while k.CmdGetCurPos() != poslist:
		print "x"
		print KHR1Serial.ACK
	poslist[5] = 180	
	#time.sleep(.3)
	
	print k.CmdSetCurPos(6, poslist)
	while k.CmdGetCurPos() != poslist:
		print "x"
		print KHR1Serial.ACK
	poslist[5] = 90
	#time.sleep(.3)
	
	print k.CmdSetCurPos(7, poslist)

	return 0

if __name__ == '__main__': main()
