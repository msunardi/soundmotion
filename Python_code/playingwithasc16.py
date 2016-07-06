#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       playingwithasc16.py
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

import serial, time, csv, readasc16
#import popen2

transcript_id={'line':0, 'onsettime':1, 'onset':2, 'onsetmax':3, 'onsetpitch':4, 'onsetintensity':5, 'onsetintensitymax':6, 'releasetime':7, 'release':8, 'releasepitch':9, 'releaseintensity':10}
gestures={'iconic': {'hline': [[1,0,0],[3,8,0],[5,8,0],[181],[1,10,0],[181]],
					 'box': [[2,8,0],[182],[5,10,0],[185],[2,2,0],[182],[5,13,0],[185],[2,8,0],[182],[5,10,0]],
					 },
		  'deictic': {'up': [[3,6,0],[5,0,0],[185]],
					  'down': [[3,8,0],[5,10,0],[185]],
					  'left': [[1,0,0],[181]],
					  'right': [[1,12,0],[181]],
					  'forward': [[3,5,0],[5,4,0],[183]],
					  'back': [[3,8,0],[5,0,0],[185]],
					  },
		  'beat': {'updown':[[5,5,0],[185],[5,10,0],[185]],		# old: [[3,7,0],[5,8,0],[183],[3,9,0],[5,6,0],[183]]
				   'leftright':[[1,4,0],[181],[1,6,0],[181]],
				   'fwdback':[[3,10,0],[5,10,0],[183],[3,0,0],[5,0,0],[183]],
				   }
		  }
home = [[1,5,0],[3,8,0],[5,4,0],[7,5,0]]
port = 'COM4'
#ser = None
ser = serial.Serial(port, 9600)
servos={'basey':1, 'basex': 2, 'neckx': 3, 'neckz':4}

def init(port=port):
	print "Opening port ", port,
	try:
		ser = serial.Serial(port, 9600)
		print "success!"
		return 1
	except:
		print "failed!"
		return 0
	

def closeSerial():
	try:
		ser.close()
		print "Port %s closed." % (port)
	except:
		print "Error closing port %s." % (port)

def go(data):
	for i in data:
		ser.write(chr(i))
	#print ord(ser.read())
		
def seriex(data, delayx=.5, tempox=500, adjx=.2):
	buffer = []
	buffer_limit = 128
	buffer_count = 0
	data_length = len(data)
	
	for i in range(data_length):
		#if isinstance(data[i], list):
		#	buffer_count += len(data[i])
		#	buffer.append(data[i])
		buffer_count += len(data[i])
		buffer.append(data[i])
		if buffer_count > buffer_limit-3 or i == data_length-1:
			serie(buffer, delay=delayx, tempo=tempox, adj=adjx)
			#print buffer			
			print "Flushing Buffer..."#, len(buffer)
			buffer = []
			buffer_count = 0
			time.sleep(.1)

def serie_simple(data):
	for i in data:
		print i
		go(i)

def serie(data, delay=.5, tempo=500, adj=.2): # tempo in miliseconds
	#print len(data)/2
	#adjust = 0
	#ser.open()
	d_t = tempo
	d_t_1 = tempo
	i_1 = -1
	c = 0
	data_ = iter(data)
	last_g = 0
	for i in data:
		t0 = time.time()		# << Let's time the execution time
		delay = abs(delay)
		print "data:", i
		print "delay:", delay
		if isinstance(i, float):
			print "rest: %f" % i
			#time.sleep(abs(i-delay))
			
		else:			
			#go(i)
			try:
				g = data_.next()
				
			except:
				print "End of line"
				break
				
			#if len(i) == 3 and i[0] in range(1,17):# and i[0] == i_1:
			while len(g) == 3 and g[0] in range(1,17):
				if g[0] == last_g: break
				print "g:",g
				go(g)
				go([180+g[0]])
				time.sleep(.05)
				last_g = g[0]
				try:
					g = data_.next()
				except:
					print "End of line"
					break
				#time.sleep(abs(delay))
			time.sleep(abs(delay))
			#go(i)
			i_1 = i[0]
			#print "i_1:", i_1
		#print ord(ser.read())
		d_t = (time.time() - t0) * 1000
		if d_t < d_t_1:
			t = d_t
		else: t = d_t_1
		print "Time: %.3f ms" % (d_t)  # print how long it takes to send one asc16 command
		
		# ADAPTIVE DELAY! MWHAHAHAAHA!!!
		if abs(d_t) > 0.5:
			if d_t < tempo:
				delay += ((tempo - d_t)/1000.)*adj
			elif d_t > tempo:
				delay -= ((d_t - tempo)/1000.)*adj
			d_t_1 = t
		c += 1
		#print "c=%d" % (c)
	#ser.close()

def readcsv(path):
	return [i for i in csv.reader(open(path))]

def onlyget(script, id):
	return [float(i[transcript_id[id]]) for i in script[1:]]	# script[1:] -> to skip the column header
	
def converttoasc16motionrange(servo_id, value):
	# 0 = [servo_id, 5, 0] (1280), 1 = [servo_id, 10, 0] (2560), -1 = [servo_id, 0, 0] (0)
	vax = float(value) + 1
	pos = int(vax*1280)
	return [servo_id, pos/256, pos%256, 3, pos/256, pos%256, 1 , pos/256, pos%256]
	
def diffdata(data):
	return [round(data[i]-data[i-1],3) for i in range(1, len(data))]

def addacceleration(data, timing, servo_id):
	temp_data = data[:]
	temp_timing = diffdata(timing)
	print len(temp_timing)
	acc = lambda x: int((1-x)*10)
	print range(1,len(temp_data))
	print len(temp_timing)
	for i in range(0,len(temp_data),2):
		#print i
		temp_data[i].insert(0, 80+servo_id)
		temp_data[i].insert(1, acc(temp_timing[i/2-1]))
	return temp_data
	
def hline():
	data = gestures['iconic']['hline']
	#go([116,5])
	serie(data)
	
def box():
	x = home[:]
	x.extend(gestures['iconic']['box'])
	serie(x)

def up():
	serie(gestures['deictic']['up'])

def down():
	serie(gestures['deictic']['down'])

def left():
	serie(gestures['deictic']['left'])

def right():
	serie(gestures['deictic']['right'])

def forward():
	serie(gestures['deictic']['forward'])

def back():
	serie(gestures['deictic']['back'])
	
def updown(repetition=3):
	serie([[85,5]])
	data1 = gestures['beat']['updown']
	data_ = data1[:]
	for i in range(repetition-1):
		data_.extend(data1)
	x=home
	x.extend(data_)
	print x
	serie(x)

def leftright(repetition=3):
	data1 = gestures['beat']['leftright']
	data_ = data1[:]
	for i in range(repetition):
		data_.extend(data1)
	x=home
	x.extend(data_)
	print x
	serie(x)

def fwdback(repetition=3):
	data1 = gestures['beat']['fwdback']
	data_ = data1[:]
	for i in range(repetition):
		data_.extend(data1)
	x=home
	x.extend(data_)
	print x
	serie(x)
	
def main():
	#ra = readasc16.readasc16()
	#ra.start()
	#fin, fout = popen2.popen2('python readasc16.py')
	path = '/home/msunardi/Downloads/praat/quickly_transcript.csv'
	script = readcsv(path)
	onset = onlyget(script,'onset')
	timing = onlyget(script, 'onsettime')
	servo_id = 5
	data = [converttoasc16motionrange(servo_id,i) for i in onset]
	#for i in range(1, len(data)*2, 2):
		#data.insert(i, [180+servo_id])
		#data.insert(i, [116, servo_id])
	#print data
	term=[0,0,0]
	
	go(term)
	#go([242])
	serie(data)
	print timing
	print diffdata(timing)
	#accldata = addacceleration(data, timing, 3)
	#serie(accldata[:10])
	#hline()
	#updown(10)
	#box()
	#forward()
	#back()
	#fwdback()
	#print fin.readline()
	#print ra.getdata()
	#ra.kill()
	
	return 0

if __name__ == '__main__':
	main()
	
class rasc16:
	def __main__(self):
		#self.fin, self.fout = popen2.popen2('python readasc16.py')
		pass
	
	def read(self):
		return self.fin.readline()
