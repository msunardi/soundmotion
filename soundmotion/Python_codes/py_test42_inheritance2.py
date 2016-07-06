#!/usr/bin/env python
#
#       py_test42_inheritance.py
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
import py_test42_inheritance as p

class a(p.a):
	def __init__(self):
		p.a.__init__(self)
		print "init x", p.A
		
		
"""		
class b(a):
	def __init__(self):
		a.__init__(self)
		print "ax: %d" % (self.ax)
	def c(self, cc = A):
		print cc
"""
def main():
	c = a()
	
	return 0

if __name__ == '__main__': main()
