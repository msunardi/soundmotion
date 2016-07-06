#!/usr/bin/env python
#
#       py_test43_time.py
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

import time

def time1():
	a = time.time()
	time.sleep(2)
	b = time.time()
	t = (b-a)*1000
	print "t: %f" % (t)

def main():
	t = time.time()
	#t = time.clock()
	print t
	time.clock()
	
	for i in range(10):
		print
		time1()
	return 0

if __name__ == '__main__': main()
