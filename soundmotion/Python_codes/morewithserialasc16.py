#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2010 msunardi <msunardi@ubuntu>
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

import serial, time

dev = '/dev/ttyUSB0'

ser = serial.Serial(dev)
servo1 = 1
servo2 = 3
servo3 = 0
servo4 = 0
#for i in ser.read(2):
#	print i
def go(data):
	for i in data:
		ser.write(chr(i))
		#ser.read(2)
		#for x in ser.read(2):
		#	print "Returned:", ord(x)
		    

def serie(data, delay=.5):
	for j in data:
		t0 = time.time()
		go(j)
		time.sleep(delay)
		print "Time: %.3f" % ((time.time() - t0)*1000)

def serie2(data, delay=.5):
	tmp = []
	f = len(data)
	data+=[[-1]]
	for i in range(f):
		if len(data[i]) == 3 and len(data[i+1]) == 3:
			tmp+=[data[i]]
			continue
		else:
			for j in tmp:
				t0 = time.time()
				go(j)
				s=j[0]
				time.sleep(delay)
				print "Time: %.3f" % ((time.time() - t0)*1000)
			
			go(data[i])

def main():
	home = [[servo1,10,0],[servo2,10,0]]
	wait = 0
	p = [[servo1,5,0],[servo2,5,0]]
	ac = [[119,2],[80+servo1,0,5],[20+servo1,5,232],[servo1,0,0],[180+servo1],[201],[80+servo1,0,3]]
	wait = [[119,1],p[1],[111,30],p[0]]
	#home.insert(1,[111,10])
	#serie2(p+home)	
	serie([[servo1,5,0],[181],[111,3,232],[servo1,10,0]])
	ser.close()
	return 0

if __name__ == '__main__':
	main()
