import multiresfilter as mrf
import numpy
import KHR1readcsv
import csv

class bandPassBands:

    def __init__(self, freq_bands_all=None):
        	
	if freq_bands_all is not None:
            self.fbands_all = []
            for i in range(len(freq_bands_all)):
                self.fbands_all.append(freq_bands_all[i][:])

    def calculateBands(self, freq_bands):
        self.fbands = []
	for i in range(len(freq_bands)-1):
            self.fbands.append(list(numpy.subtract(freq_bands[i], freq_bands[i+1])))
	
	return self.fbands

    def bringItOn(self, freq_bands_all):
	
	self.fbands_all = []             
        for bands in freq_bands_all:
            print "bands length: ",len(bands)
            self.fbands_all.append(self.calculateBands(bands))
       
        return self.fbands_all


""" ==============================================
	TESTS
    ==============================================
"""

#motion = KHR1readcsv.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#print "motion list: ", motion

#motion = [[1,3,4,5,6,7,8,9,10,42,12,53,12,10,55,12,23],[32,42,12,63,23,23,53,1,5,6,2,32,17,84,23,10,44],[12,42,22,31,9,8,4,24,1,52,12,5,12,23,7,11,20]]

"""
filt = kfilter(motion)
print "fb = ", filt.fb

filtered = []
filtered = filt.filterAll(motion)

i = 0
j = 0

for gains in filtered:
    print "Gains for Channel ", i, " : "
    for gj in gains:
        print "G_",j+1, " = ", gj
	j += 1
    j = 0
    i += 1
"""

""" ==========================================
	TEST 1: bands calculated per channel
    ==========================================
"""

#bpb = bandPassBands()

#fb = []
#fb = bpb.calculateBands(motion)

#print "Band pass filter bands = ", fb

""" ==========================================
	TEST 2: give all data (all channel bands) at once!
		let the code divide and conquer (solve) all at once
		using wimpy, mock data
    ==========================================
"""
"""motion = [[1,3,4,5,6,7,8,9,10,42,12,53,12,10,55,12,23],[32,42,12,63,23,23,53,1,5,6,2,32,17,84,23,10,44],[12,42,22,31,9,8,4,24,1,52,12,5,12,23,7,11,20]]

bpb2 = bandPassBands(motion)
print bpb2.bands_all

bands = bpb2.bringItOn()
print "Result bands: ", bands
"""
""" ==========================================
	TEST 3: give all data (all channel bands) at once!
		let the code divide and conquer (solve) all at once
		using real, manly data
    ==========================================
"""
motion = KHR1readcsv.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")

filt = mrf.kfilter(motion)
print "fb = ", filt.fb

filtered = []
filtered = filt.filterAll(motion)

bpb2 = bandPassBands()
#print bpb2.bands_all

bands = bpb2.bringItOn(filtered)
print "Result bands: ", bands

writer = csv.writer(open("test_filterbands.csv", "wb"))

for rows in bands:
    writer.writerows(rows)
