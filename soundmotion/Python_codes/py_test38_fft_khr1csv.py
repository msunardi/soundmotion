import numpy as np
from numpy import arange, pi, exp, sin
from numpy.fft import fft, fftfreq, ifft
import matplotlib.pyplot as plt
import mosynth16_p as ms

motionFilePath = ["/home/msunardi/Documents/thesis-stuff/KHR-1-motions/better_fwd_walk_data.csv", 
                  "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv",
                  "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_bird.csv",
                  "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_left.csv",
                  "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv",
                  "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backflip.csv",
                  "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backward_roll.csv",
                  "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH1.csv"]  # <<< Selected motion signals

mosynth = ms.MotionSynthesizer()

motion = mosynth.readCSV(motionFilePath[1])
print "Motion: ", motion[0]
#motion0_n = [float(i)/max(motion[0]) for i in motion[0]]
#motion1_n = [float(i)/max(motion[1]) for i in motion[1]]
#print motion0_n
intmotion = mosynth.interpolate([motion[0],motion[1]])
#intmotion = mosynth.interpolate([motion0_n,motion1_n])
print "Interpolated motion: ", intmotion

#plt.plot(motion[0])
#plt.plot(motion[1])
#plt.show()

#plt.plot(intmotion[0])
#plt.plot(intmotion[1])
#plt.show()

#im = [float(i)/max(intmotion[0]) for i in intmotion[0]]
#im = [float(i)/max(intmotion[1]) for i in intmotion[1]]
#print im
im = intmotion[0]
"""sp = fft(intmotion[0])
freq = fftfreq(len(intmotion[0]))
print sp
plt.plot(freq,abs(sp))
plt.show()"""
sp = fft(im)
freq = fftfreq(len(im))
print sp
#plt.plot(freq,abs(sp.real), freq, abs(sp.imag))
plt.plot(freq,sp.real, freq, sp.imag)
#plt.show()
#print len(im)

#sp[:100] = 0
#sp[:10] *= 0
#the fft spectrum is arranged: index[0] = average, n/2 = positive, remaining = negative
c = len(sp)/4   # c = divide the spectrum into 4 regions (positive & negative: low & high, each)
print c
sp[c:c*2] *= 0  #remove high frequencies
#sp[c:c*2] *= 10  #increase high frequencies
#sp[:c] *= 5
print sp
l = ifft(sp)
print l
#plt.plot(im)
#plt.plot(l)

plt.show()


#t = arange(256)
"""sp = fft(sin(2*pi*t))
freq = fftfreq(t.shape[-1])
print freq
sp = abs(sp)
plt.plot(freq, sp)
plt.show()
"""
#plt.plot(sin(2*50*pi*t))
#plt.show()
