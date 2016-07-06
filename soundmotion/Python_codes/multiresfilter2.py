import math
import KHR1readcsv
import numpy

""" Filtering class from Motion Signal Processing
	
	Input:
	- motion list

	Output:
	- Method: Filter
		Bandpass filter bands
	- Method: Reconstruct
		Modified motion list
"""


class kfilter:

    def __init__(self, motion_length):

	# Kernel (based on indexing [-2, -1, 0, 1, 2] - actual kernel is [1/16, 1/4, 3/8, 1/4, 1/16])
	self.kernel = [0.375, 0.25, 0.0625, 0.0625, 0.25]

	# value of k: 0 <= k < fb
	#self.frames = len(motion_list[0])
        #self.frames = motion_length
	#self.fb = int(math.log(self.frames,2))
        self.fb = int(math.log(motion_length,2))
	self.fdata = []
	self.l = 0

    #=== PREPARING DATA FOR CONVOLUTION ===
    def pad_bounds(self, data, k):

        # Padding data boundaries
	self.fdata = data
	for i in range(pow(2,k)):
	    self.fdata[0:0] = [data[0]]
 	    self.le = len(self.fdata)-1 
	    self.fdata[self.le:self.le] = [data[self.le]]
	
	self.l = 0
	return self.fdata

    def pad_bounds_once(self, data):

        # Padding data boundaries
	self.fdata = data
	for i in range(2):
	    
    	    self.fdata[0:0] = [data[0]]
	    self.le = len(self.fdata)-1
	    self.fdata[self.le:self.le] = [data[self.le]]
	
	self.l = 0
	return self.fdata
    
    #=== MAIN FILTERING ALGORITHM ===
    def filtering(self, data_in, k):
	data = []
	data = data_in[:]
	data = self.pad_bounds(data,k)
	
	self.filtdata = []
	# Get lowpass sequence
	for i in range(pow(2,k), len(data)-pow(2,k)):
    	    self.g = 0
	    for j in range(-2,3,1):

		# --- Checkpoint datapoint * kernelpoint
	        #print data[i+(pow(2, k-1)*j)], self.kernel[j]
	        self.g += data[i+(pow(2, k-1)*j)] * self.kernel[j]
            self.filtdata.append(self.g)

	    # --- Checkpoint filtered point
	    #print "-------- total: ", self.g
	
	return self.filtdata
	    
    def filterAll(self, data_all):
	
	self.tempband_all = []

	for motion in data_all:
	    self.tempband = []
	    self.tempdata = []	    
	    self.tempdata = motion[:]	# Copy the list so the original data not changed
	    self.k = 1
	     
	    # --- Checkpoint tempdata
	    #print "tempdata = ", self.tempdata

            # G0 = original data
            self.tempband.append(self.tempdata)
	   
	    while self.k < self.fb:
		self.filter = []
		# --- Checkpoint k
		#print "k = ",self.k

		# --- Checkpoint tempdata
		#print "tempdata = ", self.tempdata

		self.filter = self.filtering(self.tempdata,self.k)
		
		self.tempband.append(self.filter)
		
		# --- Checkpoint tempband
		#print "tempband = ", self.tempband
		self.k += 1
    	    
            self.tempband_all.append(self.tempband)

	return self.tempband_all

    #=== CALCULATE GAINS ===
    def getGains(self, filtereddata):
        
        self.gains_all = []

        for data in filtereddata:
            self.tempgain = []   
            for i in range(len(data)-1):
		self.again = list(numpy.subtract(data[i],data[i+1]))
                self.tempgain.append(self.again)
            self.gains_all.append(self.tempgain)

        return list(self.gains_all)


    #=== RETRIEVE ORIGINAL MOTION DATA ===
    def sumGains(self, gains):
        self.gainsum = []
        self.gainsum = gains[0]

        for i in range(len(gains)-1):
            self.gainsum = list(numpy.add(self.gainsum, gains[i+1]))
            #print "gainsum = ", list(self.gainsum)
        return self.gainsum

    def getOriginalData(self, filtered, gains):

        original = []
       
        lenf = len(filtered[0])
       
        for i in range(len(filtered)):
            original.append(list(numpy.add(filtered[i][lenf-1], self.sumGains(gains[i]))))            

        return original


    #=== ADJUST GAINS FOR INDIVIDUAL CHANNEL ===
    def adjustGain(self, gain, adjustment):

        return list(numpy.add(gain, numpy.multiply(gain, adjustment)))
            

""" ==============================================
	TESTS
    ==============================================
"""

#motion = KHR1readcsv.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")

motion = [[1,3,4,5,6,7,8,9,10,42,12,53,12,10,55,12,23],[32,42,12,63,23,23,53,1,5,6,2,32,17,84,23,10,44],[12,42,22,31,9,8,4,24,1,52,12,5,12,23,7,11,20]]

#print "motion list: ", motion

filt = kfilter(len(motion[0]))
#print "fb = ", filt.fb

filtered = []
filtered = filt.filterAll(motion)
gains = []
gains = filt.getGains(filtered)

i = 0
j = 0

for f in filtered:
    print "Frequency bands for Channel ", i, " : "
    for fj in f:
        print "FB_",j+1, " = ", fj
	j += 1
    j = 0
    i += 1
i = 0
j = 0
for g in gains:
    print "Gains for Channel ", i, " : "
    for gj in g:
        print "G_",j+1, " = ", gj
	j += 1
    j = 0
    i += 1

print "Restored motion: ", filt.getOriginalData(filtered,gains)
print "Original motion: ", motion
print "Adjusted gain[0][0] (-0.5) = ", filt.adjustGain(gains[0][0],-0.5)


"""filtered = []
filter1 = []
filter1 = filt.filtering(motion[0],1)
print "filter1 = ",filter1
filtered.append(filter1)
filter2 = []
filter2 = filt.filtering(motion[0],2)
filtered.append(filter2)
print "filtered(2) = ",filtered
filter3 = []
filter3 = filt.filtering(motion[0],3)
filtered.append(filter3)
print "filtered(3) = ",filtered
"""


#print "Original motion = ",motion

""" FOR REFERENCE ONLY!!! 
# G1
for i in range(2,len(data)-2):
    g = 0
    for j in range(-2,3,1):
	print data[i+j], kernel[j]
	g += data[i+j]*kernel[j]
    convolved.append(g)
    print "-------- total: ", g

# G2
for i in range(4,len(data2)-4):
    g = 0
    for j in range(-2,3):
	print data2[i+2*j], kernel[j]
	g += data2[i+2*j]*kernel[j]
    convolved2.append(g)
    print "-------- total: ", g

#G3
for i in range(8, len(data3)-8):
    g = 0
    for j in range(-2,3):
        print data3[i+4*j], kernel[j]
        g += data3[i+4*j]*kernel[j]
    convolved3.append(g)
    print "-------- total:", g

"""
