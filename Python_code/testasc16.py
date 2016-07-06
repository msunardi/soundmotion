#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2010 msunardi <msunardi@OODELALLY>
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
import serial, time, timeit

ser = serial.Serial('COM4')
home = [[1,9,0],[3,5,10],[5,10,10]]
term = [0,0,0]

def go():
	x = []
	for i in range(10):
		#ser.write(chr(i))
		#print "wak"
		ser.write(chr(i))
		time.sleep(0.01)
	#return 0
		
def serie(data):
	for i in data:
		go(i)
	#return 0

def test():
	"Stupid test function"
	L = []
	for i in range(10):
		L.append(i)

def main():
	t = timeit.Timer("go()", "from __main__ import go")
	print t.timeit()
	return 0



if __name__ == '__main__':

	main()

