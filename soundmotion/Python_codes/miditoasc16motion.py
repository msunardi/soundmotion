#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       miditoasc16motion.py
#       
#		Description: translating midi data to robot motion via asc16
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

import readmidi, numpy, serial
from pylab import *

PATH = '/home/msunardi/temp/lullaby_of_birdland_part_quantz.med'
TPB = 96	# ticks/beat
HOME_NOTE = 60 # note: c4

def analyzeNoteOnPerBeat(events):
	#analyze for simultaneous note strikes in a beat
	l = (events[-1][0]/96) + 2	# find the last tick, divide by 96 = # of beats.
	#print l	
	sim = []
	
	for i in range(l):
		sim_temp = []
		beat0 = (i)*TPB
		beat1 = (i+1)*TPB
		for e in events:
			if e[0] >= beat0 and e[0] < beat1:
				sim_temp.append(e)
			
		sim.append([beat0, len(sim_temp)])
	
	return sim
	
def 

def main():
	
	rm = readmidi.readmidi(PATH)
	events = rm.parseevents(ret=2)
	events_t = numpy.transpose(events)
	nopb = analyzeNoteOnPerBeat(events)
	#print nopb
	plot(numpy.transpose(nopb)[1])
	#plot(nopb)	
	#plot(events_t[0], events_t[1])
	#show()
	
	return 0

if __name__ == '__main__':
	main()
