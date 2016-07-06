#!usr/bin/python
# This is a simple metronome coded in Python, my first experience with python
# Any ideas, corrections and comments pleas email-me 
# ricardolameiro at y a h oo dot com (sorry, anti spam here)
#
#
# needs Python module  tkSnack  developed at KTH in Stockholm, Sweden
# free download: snack229-py.zip
# from: http://www.speech.kth.se/snack/
#
# This code is free, for any type of use, except commercial
# I assume I kind of GPL
# 
# (c) Ricardo Lameiro



import Tkinter
import tkSnack
import time
import sys

 
def playNote(freq, duration):
    """play a note of freq (hertz) for duration (seconds)"""
    snd = tkSnack.Sound()
    filt = tkSnack.Filter('generator', freq, 30000, 0.0, 'sine', int(11500*duration))
    snd.stop()
    snd.play(filter=filt, blocking=1)


 
def soundStop():
    """stop the sound the hard way"""
    try:
        root = root.destroy()
        filt = None
    except:
        pass



#insert Beat per minute routine
#comment if you whant to use raw inmput

ubpm = sys.argv[1]

#uncomment if want to use raw_imput

#ubpm = raw_input('Insert BPM please: ')

#protects for errors, maximum bpm is 300

Ubpm = int(ubpm)
if Ubpm > 300:
    BPM = 300

else :
    BPM = ubpm


    
#this transforms the bpm time, into a usable time delay var

bpm = 60.0 / int(BPM)

#this subtracts the time used by the sound beep, so the total delays is
# BPM = beeptime + delay

print bpm
delay = bpm - 0.1



root = Tkinter.Tk()
tkSnack.initializeSnack(root)

tkSnack.audio.play_gain(80)



#delay routine
while True:
    playNote(880, 0.1)
    soundStop()
    time.sleep(delay)




root.withdraw()  
