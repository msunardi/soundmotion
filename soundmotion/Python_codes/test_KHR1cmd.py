#!/usr/bin/env python
#
#       test_KHR1cmd.py
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


#import KHR1Serial_test as KHR1Serial
import KHR1CmdBase as KHR1Cmd
import time
from mosynth17_p import MotionSynthesizer

if __debug__ :
	print "DEBUG\n"


def main():
	defSpeed = 5
	ms = MotionSynthesizer()
	data = ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/weirdarmgesture.csv")
	cmd = KHR1Cmd.KHR1CmdBase(port="/dev/ttyUSB0")
	#print "data:", data
	for step in zip(*data):
		#print "step=", step, "length:", len(step)
		#step = self._GroomChannelList(step)
		#print "new step=", step
		# use these two when the speed is included in the data [0]
		#self.CmdSetCurPos(step[0], step[1:])	#<<< method inherited from KHR1Cmd
		#while self.CmdGetCurPos() != step[1:]:	#<<< method inherited from KHR1Cmd
		#self.CmdSetCurPos(defSpeed, step)				
		cmd.RCB1CmdSetCurPos(0, defSpeed, step[:12])
		print "."
		sys.stdout.flush()
		#print "get:", cmd.RCB1CmdGetCurPos(0)
		#print "step:", step[:12]
		#while cmd.RCB1CmdGetCurPos(0) != step[:12]:
		# wait until position is done...
			#print cmd.RCB1CmdGetCurPos(0)
			#cmd.RCB1CmdSetCurPos(0, defSpeed, step[:12])
			#time.sleep(0.01)
			#self.CmdSetCurPos(defSpeed, step)
			#print "Ack: %d" % (KHR1Serial.ACK)
		time.sleep(0.04)
		
					
	return 0

if __name__ == '__main__': main()
