import numpy as np
from numpy import arange, pi, exp, sin
from numpy.fft import fft, fftfreq, ifft
import matplotlib.pyplot as plt

t = arange(2048)
s = sin(2*pi*t)
sp = fft(sin(2*pi*t))
freq = fftfreq(t.shape[-1])
print freq
sp = abs(sp)
plt.plot(freq, sp)
#plt.plot(sp)
plt.show()
