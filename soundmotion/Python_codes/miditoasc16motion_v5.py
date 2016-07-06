# LAST WORKING STATE PER 3/28/2010
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

import readmidi, numpy, serial, playmidi#, playingwithasc16, 
from pylab import *
from subprocess import Popen
from numpy import fft
import time

PATH = '../temp/lullaby_of_birdland_part_quantz.med'
TPB = 384	# ticks/beat (was 96)
HOME_NOTE = 60 # note: c4
NOTE_RANGE = 127
RANGE_OF_MOTION = 4000	# for asc16
UP_BOUND = 9
LOW_BOUND = 3
a_MAX = 50		# max acceleration 

def analyzeNoteOnPerBeat(events):
	#analyze for simultaneous note strikes in a beat
	l = (events[-1][0]/TPB) + 2	# find the last tick, divide by 384 = # of beats.
	#print l	
	sim = []
	
	for i in range(l):
		sim_temp = []
		#v_on_temp = []
		beat0 = (i)*TPB
		beat1 = (i+1)*TPB
		for e in events:
			#print e
			if e[0] >= beat0 and e[0] < beat1:
				sim_temp.append(e)
			
			
		sim.append([beat0, len(sim_temp), sim_temp])
	
	return sim

def analyzePhrase(phrase):	
	# ^ Extract all the melodic information: 
	#	Time (ticks), beat#, prev note, next note, current note, delta (next note - curr notes), rests (breaks), sustain (T/F),
	#	melodic phrases, 
	# phrase = 16 beats, 4 bars, 4 beats/bar (assuming 4/4 timing)
	rest_count = 0
	rest_start = 0
	rest_end = 0
	curr_note = HOME_NOTE
	phrase_start = 0
	phrase_end = 0		# select the note with the longest sustain - reset if pause is detected
	is_this_rest = False # silent/pause/break/rest flag
	last_is_rest = True
	phrase_border = True
	sustain = False
	list_start = True		# << Just a flag to mark the beginning of the list to avoid out of bounds ref of the list
							# ... this will be False after the first element
	dNote = 0
	energy_from_note = 0	
	info = []
	melodic_surface = [[],[]]
	
	#Set up temporary containers
	tmp_end = 0
	tmp_contour = []
	tmp_cenergy = []
	tmp_ctime = []
	tmp_notes = []
	
	for bi in phrase:	# for each beat in the phrase
						# the phrase will be a list of beat infos [ [beatinfo0], [beatinfo1], [beatinfo2]...[beatinfon] ]
						# remember format of each phrase element (bi) beatinfo# = [ tick of beat, # of notes, [notes in the beat]]
						#		[notes in beat] = [tick, len, note, von, voff] (voff is still assumed... I don't know if this value (c) is actually voff or not) UPDATE: CONFIRMED, c = note-off
		#print "bi:", bi
		beat_tick = bi[0]		# tick
		num_of_notes = bi[1]	# number of notes in beat
		notes = bi[2]			# notes in the beat
		last_note = curr_note
				
		
		#===> 1. Check for note events or breaks
		if notes:	# if there are note-on events within the beat..
			# Record the last Break/Rest event, if any...
			if is_this_rest:
				# Record the rest/break info
				info.append({'phrase': False,
							 'rest_start': rest_start,
							 'rest_end': rest_start + (rest_count*TPB),
							 'rest_duration': rest_count,
							 'rest_energy': rest_energy})
				
				rest_count = 0		# Reset all rest variables
				rest_start = 0
				rest_energy = 0
				is_this_rest = False
				phrase_start = beat_tick
				
			# Record the longest duration of the notes (in phrase_end) - to determine SUSTAIN state
			phrase_end = max([ n[0]+n[1] for n in notes ])	# find the time the note with the longest duration in the beat will end
			sustain = True
			
			if num_of_notes == 1:
				#is_this_rest = False
				next_note = notes[0][2]		# I need the next_note info to determine the target position
				dNote = next_note - curr_note
				energy_from_note = notes[0][-2]		# Note: b[2][-2] = von	
							
			elif num_of_notes > 1:
				#is_this_rest = False
				d = [i-curr_note for i in [j[2] for j in notes]]	# << j[2] = note #
				dNotemax = max(d)
				dNotemin = min(d)
				
				# find the biggest delta Note (dNote) whether it's negative or positive deltas
				if abs(dNotemax) > abs(dNotemin): dNote = dNotemax
				else: dNote = dNotemin
				next_note = curr_note + dNote
				
				#energy_from_note = max([j[3] for j in bi[2]])	# energy is calculated as the max note-on velocity among the notes
				energy_from_note = sum([pow(j[3],2) for j in notes])/len(notes) # energy = (1/num of notes)*(sum of note on velocities)
				
						
			if phrase_end > tmp_end:
				tmp_end = phrase_end		# If the new note is longer than the last longest note, 
											# ...update the end time for the phrase			
				
			tmp_notes.append(notes)			# Collect the notes
			tmp_contour += [next_note]		# Collect the next_note (target notes) for contour (correspond with energy)
			tmp_cenergy += [energy_from_note] # Collect the 'perceived energy' in the beat (correspond with contour)
			tmp_ctime += [min([i[0] for i in notes])]
			curr_note = next_note
			continue	# Keep going...
						
		elif not notes and (beat_tick <= phrase_end):
			sustain = True
			is_this_rest = False
			continue	# Keep going...
			
		elif not notes and (beat_tick > phrase_end):	# If there are no note events, and after SUSTAIN state...
			if sustain:		# If previously it was SUSTAIN or was a phrase...
				sustain = False
				if tmp_cenergy:	rest_energy = tmp_cenergy[-1]
				else: rest_energy = 0
				info.append({'phrase': True,
							 'phrase_start': phrase_start,
							 'phrase_end': tmp_end,
							 'phrase_length': tmp_end - phrase_start,
							 'contour_amplitudes': tmp_contour,
							 'contour_energy': tmp_cenergy,
							 'contour_time': tmp_ctime,
							 'notes': tmp_notes})
				
				tmp_end = 0				# Reset all the temporary phrase variables
				tmp_contour = []
				tmp_cenergy = []
				tmp_ctime = []
				tmp_notes = []
				phrase_start = 0
			
			rest_start = beat_tick
			is_this_rest = True		# Then this must be a REST/BREAK state
			rest_count += 1				# Count REST/BREAK duration (in beats)
			next_note = curr_note
			energy_from_note = 0		# Naturally, there's no energy during REST/BREAK state
			continue	# Keep going...
			
		#if note_holds > beat_tick:  # If the note_holds value is still bigger than the current tick of the beat...				
		#	sustain = True		# Then this is a SUSTAIN state
		#else:
		#	sustain = False		# Otherwise... this is a REST/BREAK state
		#	note_holds = 0		# reset the note_holds value
						
		
		#ene = energy(num_of_notes, energy_from_note)	# energy() is a function of number of simult. notes & noteon velocity
		ene = energy_from_note
		
		if last_is_rest ^ is_this_rest: phrase_border = True
		else: phrase_border = False
		
		
		#curr_note = next_note
		
		beat = (beat_tick/384)+1
		contour = getContour(notes)
		
		info.append({'tick':beat_tick, 
					 'beat':beat, 
					 'energy':round(ene,2), 
					 'sustain':sustain, 
					 'rest': rest_count, 
					 'delta':dNote, 
					 'prev_note':last_note, 
					 'target_note':curr_note, 
					 'note-on_velocity':energy_from_note, 
					 'note_start': max([i[0] for i in notes]), # << previously min
					 'phrase_border': phrase_border, 
					 'phrase_length': phrase_end - beat_tick,
					 'contour': contour})
		
		rest_count = 0	# << setting the 'rest' count to zero must be done after the info is appended (see above line).
		last_is_rest = is_this_rest
		is_this_rest = False
		melodic_surface[0].extend( contour[0] )
		melodic_surface[1].extend( contour[1] )
	return info, melodic_surface

def getContour(notes):
	contour = [[],[]]
	for i in notes:
		#print i
		contour[0] += [i[0]]
		contour[1] += [i[2]]
	return contour
							
def energy(l,von):
	return pow(2,l) + pow(von,.5)		# you can come up with different energy function (i'm just making this one up)
 
def checkHolds(note):
	pass
	
def converts(number):
	if number < 0:
		tmp = (abs(number) ^ 65535) + 1	# ^ = XOR <-- this is two's complement process
		h = tmp/256
		if h < LOW_BOUND: h = LOW_BOUND
		elif h > UP_BOUND: h = UP_BOUND
		out = [h, tmp%256]
	else:
		h = number/256
		if h < LOW_BOUND: h = LOW_BOUND
		elif h > UP_BOUND: h = UP_BOUND
		out = [h, number%256]
	return out
	
def accel(number, servo_id=5):
	#return [80+servo_id, int((float(number)/127.)*a_MAX)]
	return [80+servo_id, int((float(number)/512.))+1]

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
		elif isinstance(d, float):
			tmp_data.append([111, int(d*100)])	# add wait for d mS
		#print tmp_data[i]
		#elif isinstance(d, float): tmp_data.append(d)
	return tmp_data

def processpos(data, servo_id):
	#-----Extract/convert phrase data to ASC16 motion------
	tempo = 127 # bpm (ONLY FOR THIS SONG!)
	timeperbeat = round(60./tempo,2)
	print 'timeperbeat', timeperbeat
	d = 0
	p = 0
	pos = []
	tmp_d = 0
	pauseflag=False
	pcount = 0
	for i in data:
		#print i
		#print len(data)
		if i['rest'] > 0:
			pauseflag=True
			pcount = i['rest']
			#print i['pause']
		else:
			if pauseflag:
				pause = pcount*(timeperbeat)
				#print "pause:", pause
				pauseflag = False
				pos.append(pause)
				pcount = 0
			
			pos.append(accel(int(i['note-on_velocity']), servo_id=servo_id))
			p = i['delta'] * i['energy']
			#print p
			if p < -4000: p = -2000		# << limit the range of motion
			elif p > 4000: p = 2000
			pos.append(converts(int(p)))
	return formatforasc16(pos, servo_id=servo_id)

def processpos2(data, servo_id, beat):
	tmp = []
	for i in data:
		if i['phrase']:		# If it's a (melodic) phrase...
							# just a reminder of the contents of phrase info: 
							# 'phrase_start', 'phrase_end', 'phrase_length', 'contour_amplitudes', 'contour_energy',
							# 'contour_time', 'notes'
			p_data = numpy.multiply(i['contour_amplitudes'], i['contour_energy'])
			p_data_ = [converts(int(p)) for p in p_data]
			#print "p_data_", p_data_
			#tmp.extend([accel(j, servo_id) for j in i['contour_energy']])
			if i['contour_energy'] != []: tmp.extend([accel(i['contour_energy'][0], servo_id)])
			tmp.extend(p_data_)
		
		else:				# Otherwise it's a rest (phrase).
			tmp.extend([i['rest_duration']*beat])
	
	
	return tmp

def processScenario(m_surface, scenario, servo_id, beat, mode=0):
	tmp = []
	m_data = []
	#l = len(m_surface)
	s = len(scenario)
	ms_index = -1	
	
	for i in range(s):	# << the augmented gestures can only be as long as the scenario length
		p_data = []
		#m_data = []
		p_data_tmp = []
		mapped = False
		r = 0
		#l = len(scenario[i])
		l = len(scenario[i])
		print "length:", l
		"""if m_surface[i]['phrase'] and m_surface[i]['notes'] != []:		# If it's a (melodic) phrase...
							# just a reminder of the contents of phrase info: 
							# 'phrase_start', 'phrase_end', 'phrase_length', 'contour_amplitudes', 'contour_energy',
							# 'contour_time', 'notes'
			p_data = numpy.multiply(m_surface[i]['contour_amplitudes'], m_surface[i]['contour_energy'])
			p_data_ = [converts(int(p)) for p in p_data]
			print "scenario[%d] = " % (i), scenario[i]
			print "m_surface[%d] = " % (i), m_surface[i]
			p_data_tmp = fft.ifft(numpy.add(fft.rfft(scenario[i], n=l), fft.rfft(p_data_, n=l)))
			
			print p_data_tmp			
			
			if m_surface[i]['contour_energy'] != []: tmp.extend([accel(m_surface[i]['contour_energy'][0], servo_id)])
			tmp.extend(p_data_tmp)
		
		elif not m_surface[i]['phrase']:				# Otherwise it's a rest (phrase).
			tmp.extend([m_surface[i]['rest_duration']*beat])
		else: continue
		"""
	
		
		while not mapped:
			ms_index += 1
			if m_surface[ms_index]['phrase'] and m_surface[ms_index]['phrase_length'] != 0 and len(m_surface[ms_index]['contour_amplitudes']) > (l/2):
				 
				print m_surface[ms_index]
				#p_data = fft.irfft(fft.rfft(scenario[i], l)*fft.rfft(m_surface[ms_index]['contour_amplitudes'], l))
				p_data = fft.irfft(numpy.multiply(fft.rfft(scenario[i], l), .02*(fft.rfft(m_surface[ms_index]['contour_amplitudes'], l)[2])))#(numpy.multiply(m_surface[ms_index]['contour_amplitudes'], m_surface[ms_index]['contour_energy']), l)))
				mapped = True
				print "pdata:",p_data
				m_data.append(m_surface[ms_index]['contour_amplitudes'])
				break
			elif m_surface[ms_index]['phrase'] == False:
				#print m_surface
				#p_data = 'rest'
				#tmp.append(m_surface[ms_index]['rest_duration'])
				r += m_surface[ms_index]['rest_duration']
				print "rest"
		tmp.append(r)		
		tmp.append(p_data)		
	
	#print tmp
	return tmp, m_data

def combine(data1, data2):	# right now for demo, assume only two data
	"""l = len(data)	#<<< this process is if input parameter is only 'data' with arbitrary number of list elements
	max_l = 0
	bin = []
	l1 = []
	tmp_l1 = []
	for i in range(l):
		if len(data[i]) > max_l: 
			max_l = len(data[i])
			tmp_l1 = l1[:]			
			l1 = data[i]			
		else:
			tmp_l1 = data[i]
		if tmp_l1 != []:
			bin.append(tmp_l1)
	"""
	if not data1 or not data2:
		return 0
		
	if len(data1) >= len(data2):
		l1 = data1
		l2 = data2
	else:
		l1 = data2
		l2 = data1
	
	#print "l1=", l1
	#print "l2=", l2
	tmp = []
	l1_ = iter(l1)
	l2_ = iter(l2)
	for i in range(len(l1)-1):
		#print i
		tmp.append(l1_.next())
		if i < len(l2):
			tmp.append(l2_.next())
		#tmp.append([111,100])
	
	return tmp
		
	

def main():
	bar = 16 #(beats/bar)
	#rm = readmidi.readmidi(PATH)
	r = readmidi.readmidi()
	
	rm = r.openfile(PATH)
	events = r.parseevents(ret=2)
	events_t = numpy.transpose(events)
	nopb = analyzeNoteOnPerBeat(events)
	#print [i[1] for i in nopb]
	#print nopb[:10]
	#for i in nopb[:10]:
	#	print i
	x = 0
	#phrase = nopb[bar*x:bar*(x+1)]
	phrase = nopb
	#print phrase
	analysis, surface = analyzePhrase(phrase)	# << this is where the information extraction happens
	#print surface
	#print type(analysis)
	#print analysis[:10]
	#for i in analysis[100:104]:
	print "analysislen:", len(analysis)
	#for i in analysis:
	#	print i
		#plot(numpy.divide(i['contour'][0],float(TPB)),i['contour'][1])
		#show()
	
	print "analysis4:", analysis[2]
	#plot(analysis[2]['contour_time'], analysis[2]['contour_amplitudes'])#numpy.multiply(analysis[8]['contour_energy'], analysis[8]['contour_amplitudes']))
	#plot(numpy.divide(analysis[4]['contour'][0],float(TPB)),analysis[4]['contour'][1])
	#print surface
	#plot(surface[0],surface[1])
	#show()
	
	#rm_beat = readmidi.readmidi('../temp/lullaby_of_birdland_drum.med')
	rm_beat = r.openfile('../temp/lullaby_of_birdland_drum.med')
	events_drum = r.parseevents(ret=2)
	#print events_drum
	events_drum_t = numpy.transpose(events_drum)
	nopb_drum = analyzeNoteOnPerBeat(events_drum)
	analysis_drum, surface_drum = analyzePhrase(nopb_drum)
	
	#for i in analysis_drum[:10]:
		#print 
	tempo = 127 # bpm (ONLY FOR THIS SONG!)
	timeperbeat = round(60./tempo,2)
	print 'timeperbeat', timeperbeat
	
	chan3 = processpos2(analysis, servo_id=9, beat=timeperbeat)
	#chan5 = processpos2(analysis, servo_id=5, beat=timeperbeat)
	print "chan3len: ", len(chan3)
	chan5 = processpos2(analysis_drum, servo_id=7, beat=timeperbeat)
	
	scenario=[[132,30,20,40],[54,120,54,126],[44,1,20,55,100,20],[10,20,32,24,8,9]]
	nyah, m = processScenario(analysis,scenario,servo_id=9, beat=timeperbeat)
	#chan5 = processpos(analysis, serv_id=5)
	#print "chan5: %d, chan3: %d" % (len(chan5), len(events_drum_t[0]))
	chan3_ = formatforasc16(chan3, servo_id=9)
	chan5_ = formatforasc16(chan5, servo_id=7)
	molist = combine(chan5_,chan3_)
	
	#-----Plotting----
	s0 = scenario[-2]
	n1 = nyah[-3]
	x = range(len(s0))
	print s0
	print n1
	print x
	print m
	time.sleep(1)
	plot(x,s0,x,n1)
	show()
	
	
	#molist = chan3_
	#print chan3
	#for i in molist[:30]:
	#	print i
	"""
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
			pos.append(accel(int(i['note-on_velocity']), servo_id=5))
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
	#-----------------------------------------------------"""
	#molist = formatforasc16(pos, servo_id=5)		# << uncomment this to run on robot
	#molist = formatforasc16(chan3, servo_id=5)
	#molist = formatforasc16(molist, servo_id=5)
	
	#molist = [converts(i) for i in pos]
	
	#for i in range(len(molist)):
	#	molist[i].insert(0,47)
	#for i in range(1,len(molist)*2,2):
	#	molist.insert(i,[187])
	
	#print molist[:20]
	#print "molist:", molist
	#for i in molist:
	#	print "data:", i
	for i in nyah:
		print "data:", i
	
	#playingwithasc16.serie([[5,15,160],[185]])
	#pid = Popen(["python", "playmidi.py"])	# << uncomment to midi
	#playingwithasc16.serie(molist)		# << uncomment to run on robot
	#playingwithasc16.serie([[3,10,0],[5,10,0]])
	#while True:
	#	continue
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
