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

    def __init__(self, motion_list):

	# Kernel (based on indexing [-2, -1, 0, 1, 2]
	self.kernel = [0.375, 0.25, 0.0625, 0.0625, 0.25]

	# value of k: 0 <= k < fb
	self.frames = len(motion_list[0])
	self.fb = int(math.log(self.frames,2))
	self.fdata = []
	self.l = 0


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
	   
	    while self.k < self.fb:
		self.filter = []
		# --- Checkpoint k
		print "k = ",self.k

		# --- Checkpoint tempdata
		print "tempdata = ", self.tempdata

		self.filter = self.filtering(self.tempdata,self.k)
		
		self.tempband.append(self.filter)
		
		# --- Checkpoint tempband
		#print "tempband = ", self.tempband
		self.k += 1
    	    
            self.tempband_all.append(self.tempband)

	return self.tempband_all


""" ==============================================
	TESTS
    ==============================================
"""

motion = KHR1readcsv.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#print "motion list: ", motion

#motion = [[1,3,4,5,6,7,8,9,10,42,12,53,12,10,55,12,23],[32,42,12,63,23,23,53,1,5,6,2,32,17,84,23,10,44],[12,42,22,31,9,8,4,24,1,52,12,5,12,23,7,11,20]]

filt = kfilter(motion)
print "fb = ", filt.fb

filtered = []
filtered = filt.filterAll(motion)

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

i = 0
j = 0

for gains in filtered:
    print "Gains for Channel ", i, " : "
    for gj in gains:
        print "G_",j+1, " = ", gj
	j += 1
    j = 0
    i += 1

print "Original motion = ",motion

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
