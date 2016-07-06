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

import readmidi, numpy, serial, playingwithasc16, playmidi
from pylab import *
from subprocess import Popen

PATH = '/home/msunardi/temp/lullaby_of_birdland_part_quantz.med'
TPB = 384	# ticks/beat (was 96)
HOME_NOTE = 60 # note: c4
NOTE_RANGE = 127
RANGE_OF_MOTION = 4000	# for asc16
a_MAX = 100		# max acceleration 

def analyzeNoteOnPerBeat(events):
	#analyze for simultaneous note strikes in a beat
	l = (events[-1][0]/TPB) + 2	# find the last tick, divide by 96 = # of beats.
	#print l	
	sim = []
	
	for i in range(l):
		sim_temp = []
		#v_on_temp = []
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
	
	note_holds = 0		# select the note with the longest sustain - reset if pause is detected
	is_this_break = False # silent/pause flag
	sustain = False
	dNote = 0
	energy_from_note = 0
	info = []
	for bi in phrase:	# for each beat in the phrase
						# the phrase will be a list of beat infos [ [beatinfo0], [beatinfo1], [beatinfo2]...[beatinfon] ]
						# remember format of each phrase element (bi) beatinfo# = [ tick of beat, # of notes, [notes in the beat]]
						#		[notes in beat] = [tick, len, note, von, voff] (voff is still assumed... I don't know if this value (c) is actually voff or not) UPDATE: CONFIRMED, c = note-off
		#print "bi:", bi
		beat_tick = bi[0]		# tick
		num_of_notes = bi[1]	# number of notes in beat
		notes = bi[2]			# notes in the beat
		
		last_note = curr_note
		#print "notes:", notes
		
		if notes:
			note_holds = max([ n[0]+n[1] for n in notes ])	# max of noteoff for each note in the beat			
		if note_holds > beat_tick:
			sustain = True
			tmp_silent = 0
		else: 
			sustain = False
			note_holds = 0
		
				
		if num_of_notes == 1:
			is_this_break = False
			next_note = notes[0][2]		# I need the next_note info to determine the target position
			dNote = next_note - curr_note
			energy_from_note = notes[0][-2]		# Note: b[2][-2] = von	
				
			#ene = energy(num_of_notes, bi[2][-2])
			#note_off = 
		elif num_of_notes > 1:
			is_this_break = False
			d = [i-curr_note for i in [j[2] for j in bi[2]]]
			dNotemax = max(d)
			dNotemin = min(d)
			# find the biggest delta Note (dNote) whether it's negative or positive deltas
			if abs(dNotemax) > abs(dNotemin): dNote = dNotemax
			else: dNote = dNotemin
			next_note = curr_note + dNote
			
			energy_from_note = max([j[3] for j in bi[2]])	# energy is calculated as the max note-on velocity among the notes
			#ene = energy(num_of_notes, max([i for i in [j[3] for j in bi[2]]]))
		elif num_of_notes < 1 and not sustain:
			is_this_break = True
			tmp_silent += 1
			next_note = curr_note
			energy_from_note = 0
		ene = energy(num_of_notes, energy_from_note)	# energy() is a function of number of simult. notes & noteon velocity
		#dNote = next_note - curr_note
		curr_note = next_note
		#next_pos = ((dNote/NOTE_RANGE) * RANGE_OF_MOTION)
		#curr_note = next_note		"""	
		beat = (beat_tick/384)+1
		#print "beat_tick:", beat_tick, "beat:", beat, "numofnotes:", num_of_notes, "energy_from_note", round(ene,2), "notes", notes, "note sustain?", sustain, "(%d)" % (note_holds), "pause/silent?", tmp_silent, "dNote:", dNote, "current_note", curr_note
		info.append({'beat_tick':beat_tick, 'beat':beat, 'energy':round(ene,2), 'note_hold':sustain, 'pause': tmp_silent, 'delta':dNote, 'prev_note':last_note, 'target_note':curr_note, 'note-on_velocity':energy_from_note})
	return info
		
			
def energy(l,von):
	return pow(2,l) + pow(von,.5)		# you can come up with different energy function (i'm just making this one up)
 
def checkHolds(note):
	pass
	
def converts(number):
	if number < 0:
		tmp = (abs(number) ^ 65535) + 1	# ^ = XOR
		h = tmp/256
		if h > 10: h = 9
		out = [h, tmp%256]
	else:
		h = number/256
		if h > 10: h = 9
		out = [h, number%256]
	return out
	
def accel(number, servo_id=5):
	return [80+servo_id, int((float(number)/127.)*a_MAX)]

def formatforasc16(data, servo_id=5):
	tmp_data = []
	for i, d in enumerate(data):
		if isinstance(d, list) and d[0]-servo_id != 80:
			#print d, i
			#d.insert(0,40+servo_id)	# for move relative
			d.insert(0,servo_id)		# for move absolute
			tmp_data.append(d)
			tmp_data.append([180+servo_id])
			#tmp_data.append([111, 47])		# add wait for a beat 47mS
		elif isinstance(d, list) and d[0]-servo_id == 80:
			tmp_data.append(d)
		#elif isinstance(d, float):
		#	tmp_data.append([111, int(d*100)])	# add wait for d mS
		#print tmp_data[i]
		elif isinstance(d, float): tmp_data.append(d)
	return tmp_data

def main():
	bar = 16 #(beats/bar)
	rm = readmidi.readmidi(PATH)
	events = rm.parseevents(ret=2)
	events_t = numpy.transpose(events)
	nopb = analyzeNoteOnPerBeat(events)
	#print [i[1] for i in nopb]
	#print nopb[:10]
	x = 0
	#phrase = nopb[bar*x:bar*(x+1)]
	phrase = nopb
	#print phrase
	analysis = analyzePhrase(phrase)
	#print type(analysis)
	#print analysis[:10]
	#for i in analysis[:10]:
		#print i
	tempo = 127 # bpm (ONLY FOR THIS SONG!)
	timeperbeat = round(60./tempo,2)
	print 'timeperbeat', timeperbeat
	
	#-----Extract/convert phrase data to ASC16 motion------
	d = 0
	p = 0
	pos = []
	tmp_d = 0
	pauseflag=False
	pcount = 0
	for i in analysis:
		#print i
		if i['pause'] > 0:
			pauseflag=True
			pcount = i['pause']
			#print i['pause']
		else:
			if pauseflag:
				pause = pcount*(timeperbeat)
				#print "pause:", pause
				pauseflag = False
				pos.append(pause)
				pcount = 0
			#d = i['delta']
			#tmp_d = d
			#p = d * i['energy']
			pos.append(accel(int(i['note-on_velocity'])))
			p = i['delta'] * i['energy']
			#print p
			if p < -4000: p = -1000
			elif p > 4000: p = 1000
			pos.append(converts(int(p)))
			
		#pos.append(int(p))
	#pos = [int(i['delta']*i['energy']) for i in analysis]
	#print pos
	#for i in pos[:10]:
	#	print i
	#-----------------------------------------------------
	molist = formatforasc16(pos)		# << uncomment this to run on robot
	#molist = [converts(i) for i in pos]
	
	#for i in range(len(molist)):
	#	molist[i].insert(0,47)
	#for i in range(1,len(molist)*2,2):
	#	molist.insert(i,[187])
	
	#print molist
	
	
	
	#playingwithasc16.serie([[5,15,160],[185]])
	pid = Popen(["python", "playmidi.py"])
	playingwithasc16.serie(molist)		# << uncomment to run on robot
	
	#pos = 0
	#for i in analysis:
		#print i
		#pos = i['delta'] * i['energy']
		#print 'pos=',pos
		
	#plot(numpy.transpose(nopb)[1])
	
	#plot(nopb)	
	#plot(events_t[0], events_t[1])
	#show()
	
	return 0

if __name__ == '__main__':
	main()
