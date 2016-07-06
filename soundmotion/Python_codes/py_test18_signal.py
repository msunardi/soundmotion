from math import *
from Numeric import *

x = arange(256.0)
sig = []

for i in range(256):
    sig.append(sin(2*pi*(1250.0/10000.0)*x[i]) + sin(2*pi*(625.0/10000.0)*x[i]))

print sig
