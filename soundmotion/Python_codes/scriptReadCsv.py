#!/usr/bin/env python
#
#       scriptReadCsv.py
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

import csv

class readScript:
	def __init__(self):
		pass
	
	def read(self, csv_path):
		# read .csv file and populate list
		return [line for line in csv.reader(open(csv_path).readlines())]

# --- FOR TESTING.....        
def main():
	rs = readScript()
	a = rs.read('scripts/script1.csv')
	print a[0][1]
	return 0

if __name__ == '__main__': main()
