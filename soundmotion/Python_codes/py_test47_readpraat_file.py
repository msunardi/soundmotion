#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       py_test47_readpraat_file.py
#       Description: reading Praat's pitch/intensity text file
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

import csv

def read(path):
	return [map(getval, line[0].split()) for line in csv.reader(open(path))]
	
def getval(x):
	try:
		return float(x)
	except:
		return 0
		
def evaldata(data):
	data = data[1:]
	print "max:", max(i[1] for i in data)
	print "min:", min(i[1] for i in data)

def main():
	
	pitch_data = read('/home/msunardi/Downloads/praat/hats_pitch.csv')
	print "Data=", pitch_data
	intensity_data = read('/home/msunardi/Downloads/praat/hats_intensity.csv')
	print "Data2=", intensity_data
	evaldata(pitch_data)
	evaldata(intensity_data)
	
	return 0

if __name__ == '__main__':
	main()
