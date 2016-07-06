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

import thread, threading, serial

class readasc16(threading.Thread):
	
	def __init__(self):
		self.flag = True
		self.readdata = [None, None]
		threading.Thread.__init__(self)	
	
	def run(self):
		x = 0
		ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
		while self.flag:
			#x += 1
			#for i in s = ser.read()
			s = ser.read()
			if s: 
				#print 's=',ord(s)
				self.readdata[0]=ord(s)
			else: print '.',
			ss = ser.read()
			if ss: 
				#print 'ss=',ord(ss)
				self.readdata[1]=ord(ss)
				#self.kill()
				print "data=", self.readdata
				
			else:
				self.readdata = [None, None]
			#if x > 10000: self.flag = False
			#print "data=", self.readdata
		print 'killed.'
		
	def getdata(self):
		return self.readdata
	
	def kill(self):
		self.flag = False
		print 'killing thread...',

def main():
	s = readasc16()
	s.run()
	#s.kill()
	
	return 0

if __name__ == '__main__':
	main()
