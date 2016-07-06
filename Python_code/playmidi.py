#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   untitled.py
#	   
#	   Copyright 2010 msunardi <msunardi@ubuntu>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.

#
import pygame, time
#
import base64
#
 
#
def play_music(music_file):
	"""
	stream music with mixer.music module in blocking manner
	this will stream the sound from disk while playing
	"""
	
	clock = pygame.time.Clock()
	try:
		pygame.mixer.music.load(music_file)
		print "Music file %s loaded!" % music_file
	except pygame.error:
		print "File %s not found! (%s)" % (music_file, pygame.get_error())
		return
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		#print pygame.mixer.music.get_pos()
		
		# check if playback has finished
		clock.tick(30)

def playmidi(music_file = '../temp/lullaby_of_birdland_drum2.mid'):
	pygame.mixer.init()
	pygame.mixer.music.set_volume(0.8)
	
	try:
		# use the midi file you just saved
		play_music(music_file)
	except KeyboardInterrupt:
		# if user hits Ctrl/C then exit
		# (works only in console mode)
		pygame.mixer.music.fadeout(1000)
		pygame.mixer.music.stop()
		raise SystemExit

def main():
	freq = 44100	# audio CD quality
	bitsize = 16   # unsigned 16 bit
	channels = 2	# 1 is mono, 2 is stereo
	buffer = 1024	# number of samples
	#pygame.mixer.init(freq, bitsize, channels, buffer)
	pygame.mixer.init()
	
	# optional volume 0 to 1.0
	pygame.mixer.music.set_volume(0.8)
	pygame.mixer.music.set_endevent()
	#music_file = '../temp/lullaby_of_birdland.mid'
	music_file = '../temp/lullaby_of_birdland_part_quantz.mid'
	#music_file = '../temp/beethoven-5th_part1.mid'
	try:
		time.sleep(2)
		# use the midi file you just saved
		play_music(music_file)
		print pygame.mixer.music.get_endevent()
	except KeyboardInterrupt:
		# if user hits Ctrl/C then exit
		# (works only in console mode)
		pygame.mixer.music.fadeout(1000)
		pygame.mixer.music.stop()
		raise SystemExit
	return 0

if __name__ == '__main__':
	main()
