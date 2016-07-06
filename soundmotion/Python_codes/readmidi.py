#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       readmidi.py
#       read Muse MIDI Sequencer .med file to get the note events: 
#			note time (ticks), note duration (len), note number (a), note on velocity(?) (b), note off velocity (c)
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

import re, numpy, os.path
from xml.dom import minidom
from pylab import *

class readmidi:
			
	def __init__(self):
		pass
	
	def openfile(self, path):
		
		self.ext = os.path.splitext(path)
		if self.ext[1] == '.med':
			print "extension: %s" % (self.ext[1])
			midiinfo = minidom.parse(path)
			#topchild = midiinfo.firstChild
			#cn3 = topchild.childNodes[3]
			#cn3_35 = cn3.childNodes[35]
			#cn3_35_41 = cn3_35.childNodes[41]
			#self.events = [i.toxml().strip() for i in cn3_35_41.childNodes[9:]]
			self.events = [i.toxml().strip() for i in midiinfo.getElementsByTagName('event')]
			
			#print events[9]
			#for i in cn3_35_41.childNodes:
			#	print i.toxml(),
			#print events
			#self.parseevents(events)
		elif self.ext[1] == '.txt':
			print 'Quack!'
			self.miditxt = open(path)
		
	def parseevents(self, ret=0):
		if self.ext[1] == '.med':
			pat_tick = re.compile('tick="(\d*)"')	# time - 1 beat = 96 ticks, 1 bar = 4 beats (usually, in pop/jazz), 1 measure = 4 bars = 1536 ticks
			pat_le = re.compile('len="(\d*)"')		# duration of a note
			pat_a = re.compile('a="(\d*)"')			# note number
			pat_b = re.compile('b="(\d*)"')			# note on velocity
			pat_c = re.compile('c="(\d*)"')			# (not sure) note off velocity? - sometimes it doesn't exist in the event when it's = 0
			tmp_events = {}
			list_events = []				# 2-D list; 'row fields' (in order): tick, len, note (a), note on (b), note off (c)
			try:
				print len(self.events)
				c = 0
				for i in self.events:
					#print i
					tick = pat_tick.search(i)
					le = pat_le.search(i)
					a = pat_a.search(i)
					b = pat_b.search(i)
					c = pat_c.search(i)
					
					if le:							# If len does not exist; i.e. not a note event					
						tick_ = int(tick.group(1))
						le_ = int(le.group(1))
						#a_ = int(a.group(1))
						b_ = int(b.group(1))
						#c_ = int(c.group(1))
						
						if not a:
							a_ = 0							
						else:
							a_ = int(a.group(1))								
						if not c:
							c_ = 0
						else:
							c_ = int(c.group(1))
						
						tmp_events[tick_] = {'len':le_, 'a':a_, 'b':b_, 'c':c_}
						list_events.append([tick_, le_, a_, b_, c_])
						
						
				if ret==0:
					return tmp_events, list_events
				elif ret==1:
					return tmp_events
				elif ret==2:
					return list_events
				else:
					print "Ha ha ha, nice try."
			except:
				print 'fail in parseevents'
		
		elif self.ext[1] == '.txt':
			pat_time = re.compile('Time=(\d*)  (Parameter|Pitchbend|Note on|Note off), chan=(\d*) (pitch|msb|c1)=(\d*) (vol|lsb|c2)=(\d*)', re.IGNORECASE)
			for i in self.miditxt:
				print pat_time.findall(i)
			
	

def main():
	#path = '/home/msunardi/temp/lullaby_of_birdland_part_quantz.med'
	path = '/home/msunardi/temp/lullaby_of_birdland_part.med'
	#path = '/home/msunardi/temp/lullaby_of_birdland_drum.med'
	#path = '/home/msunardi/temp/lullaby_of_birdland.txt'
	#rm = readmidi(path)
	r = readmidi()
	rm = r.openfile(path)
	events = r.parseevents(ret=2)
	events = numpy.transpose(events)
	#plot(events[3])
	#show()
	#print events
	#print len(events[0])
	return 0

if __name__ == '__main__':
	main()
