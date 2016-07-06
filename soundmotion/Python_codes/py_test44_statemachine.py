#!/usr/bin/env python
#
#       py_test44_statemachine.py
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

def stateA():
	x = 0
	while x != 1 and x !=2:
		x = int(raw_input('A> '))		
	if x==1:
		return stateB
	else:
		return stateC

def stateB():
	x = 0
	while x != 1 and x !=2:
		x = int(raw_input('B> '))
	if x==1:
		return stateC
	else:
		return stateA
		
def stateC():
	x = 0
	while x != 1 and x !=2:
		x = int(raw_input('C> '))
	if x==1:
		return stateA
	else:
		return stateB

def main():
	state = stateA()
	while True:
		state = state()
	
	return 0

if __name__ == '__main__': main()
