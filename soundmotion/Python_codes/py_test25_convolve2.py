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

    def filtering(self, data, k):
	
	self.tempdata = []
	# Get lowpass sequence
	for i in range(pow(2,k), len(data)-pow(2,k)):
    	    self.g = 0
	    for j in range(-2,3,1):
	        print data[i+(pow(2, k-1)*j)], kernel[j]
	        self.tempdata += data[i+(pow(2, k-1)*j)]*kernel[j]
                self.tempdata.append(g)
	    print "-------- total: ", self.g
	
	return tempdata
	    
    def filterAll(self, data_all):
	
	self.tempband_all = []

	for l in range(len(data_all)):
	    self.tempband = []
	    self.tempbandL = []
	    self.k = 1	
	    self.datax = []

	    for ll in l:
		self.datax.append(l)
	    
	    while self.k < self.fb:
		
		print "k = ",self.k
		data_all[l] = self.pad_bounds(data_all[l],self.k)
		print "data_all[",l,"] = ",data_all[l]	
		self.tempdata = []
	        for i in range(pow(2,self.k), len(data_all[l])-pow(2,self.k)):
    	            self.g = 0
	            for j in range(-2,3):
	                #print data_all[l][i+int(pow(2, self.k-1)*j)], self.kernel[j]
	                self.g += data_all[l][i+int(pow(2, self.k-1)*j)]*self.kernel[j]
                    self.tempdata.append(self.g)
	            print "-------- total: ", self.g
		print "Tempdata: ", self.tempdata
		self.tempband.append(self.tempdata)	
		self.k += 1

	    print "Tempband: ", self.tempband
	    	    
	    """for m in range(len(self.tempband)-1):
		print "tempband[",m,"]: ", self.tempband[m]
		print "tempband[",m,"]: ", self.tempband[m+1]
		#self.tempbandL.append(list(numpy.subtract(self.tempband[m],self.tempband[m+1])))
	    """
	    self.tempband_all.append(self.tempband)

	return self.tempband_all


""" ==============================================
	TEST
    ==============================================
"""

#motion = KHR1readcsv.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#print "motion list: ", motion

motion = [[1,3,4,5,6,7,8,9,10,42,12,53,12,10,55,12,23],[32,42,12,63,23,23,53,1,5,6,2,32,17,84,23,10,44],[12,42,22,31,9,8,4,24,1,52,12,5,12,23,7,11,20]]

filt = kfilter(motion)
print "fb = ", filt.fb

filtered = []
filtered = filt.filterAll(motion)

#print filtered[0]
print motion

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
