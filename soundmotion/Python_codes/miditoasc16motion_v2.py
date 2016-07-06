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
TPB = 384	# ticks/beat (was 96)
HOME_NOTE = 60 # note: c4
NOTE_RANGE = 127
RANGE_OF_MOTION = 4000	# for asc16

def analyzeNoteOnPerBeat(events):
	#analyze for simultaneous note strikes in a beat
	l = (events[-1][0]/TPB) + 2	# find the last tick, divide by 96 = # of beats.
	#print l	
	sim = []
	
	for i in range(l):
		sim_temp = []
		beat0 = (i)*TPB
		beat1 = (i+1)*TPB
		for e in events:
			if e[0] >= beat0 and e[0] < beat1:
				sim_temp.append(e)
			
		sim.append([beat0, len(sim_temp), sim_temp])
	
	return sim

def analyzePhrase(phrase):
	# phrase = 16 beats, 4 bars, 4 beats/bar (assuming 4/4 timing)
	tmp_silent = 0
	curr_note = HOME_NOTE
	note_holds = 0		# select the note with the longest hold - reset if pause is detected
	is_this_pause = False # silent/pause flag
	hold = False
	dNote = 0
	for bi in phrase:	# for each beat in the phrase
						# the phrase will be a list of beat infos [ [beatinfo0], [beatinfo1], [beatinfo2]...[beatinfon] ]
						# remember format of each phrase element (bi) beatinfo# = [ tick of beat, # of notes, [notes in the beat]]
						#		[notes in beat] = [tick, len, note, von, voff] (voff is still assumed... I don't know if this value (c) is actually voff or not)
		print "bi:", bi
		beat_tick = bi[0]
		num_of_notes = bi[1]
		notes = bi[2]
		
		if notes:
			note_holds = max([ n[0]+n[1] for n in notes ])	# max of noteon + len for each note in the beat			
		if note_holds > beat_tick:
			hold = True
		else: 
			hold = False
			note_holds = 0
		
				
		if num_of_notes == 1:
			is_this_pause = False
			next_note = bi[2][2]		# I need the next_note info to determine the target position
			dNote = next_note - curr_note
			energy_from_note = bi[2][-2]		# Note: b[2][-2] = von	
				
			#ene = energy(num_of_notes, bi[2][-2])
			#note_off = 
		elif num_of_notes > 1:
			is_this_pause = False
			d = [i-curr_note for i in [j[2] for j in bi[2]]]
			dNotemax = max(d)
			dNotemin = min(d)
			# find the biggest delta Note (dNote) whether it's negative or positive deltas
			if abs(dNotemax) > abs(dNotemin): dNote = dNotemax
			else: dNote = dNotemin
			next_note = curr_note + dNote
			
			energy_from_note = max([i for i in [j[3] for j in bi[2]]])			
			#ene = energy(num_of_notes, max([i for i in [j[3] for j in bi[2]]]))
		elif num_of_notes < 1 and not hold:
			#is_this_pause = True
			tmp_silent += 1
			next_note = curr_note
		#ene = energy(num_of_notes, energy_from_note)	
		#dNote = next_note - curr_note
		curr_note = next_note
		#next_pos = ((dNote/NOTE_RANGE) * RANGE_OF_MOTION)
		#curr_note = next_note		"""	
		print "beat_tick:", beat_tick, "numofnotes:", num_of_notes, "notes", notes, "note hold?", hold, "(%d)" % (note_holds), "dNote:", dNote, "current_note", curr_note
		
			
def energy(l,von):
	return pow(2,l) + pow(von,.5)		# you can come up with different energy function (i'm just making this one up)
 
def checkHolds(note):
	pass

def main():
	bar = 16 #(beats/bar)
	rm = readmidi.readmidi(PATH)
	events = rm.parseevents(ret=2)
	events_t = numpy.transpose(events)
	nopb = analyzeNoteOnPerBeat(events)
	#print [i[1] for i in nopb]
	print nopb[:10]
	x = 1
	phrase = nopb[bar*x:bar*(x+1)]
	print phrase
	analyzePhrase(phrase)
	#plot(numpy.transpose(nopb)[1])
	
	#plot(nopb)	
	#plot(events_t[0], events_t[1])
	#show()
	
	return 0

if __name__ == '__main__':
	main()
