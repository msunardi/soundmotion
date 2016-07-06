""" ---------------------------------------------------
	KHR1_re_in_cv.py

	Function:
	- (re) read KHR-1 motion from .csv file
	- (in) does interpolation of the motion
	- (cv) does multiresolution filtering of the interpolated motion

        Modules:
	- KHR1readcsv:	read .csv motion file, and format it into a 2-D tuple: a list of KHR-1 channels, and each element is a list of motion for the channel
	- interpolation: interpolate points
        - multiresfilter: multiresolution filtering

    ---------------------------------------------------
"""


import KHR1readcsv as motion
import interpolation
import multiresfilter
import csv


#==== READ CSV ===
"""
    already built in module KHR1readcsv
    when read, returns an list of lists (2-D list).
	The list is organized so each element of the list (which is also a list) is the motion of a channel/servo
"""

#==== INTERPOLATION  ===

interp = interpolation.hermiteInterpolate

def interpolate( motion_list, bias=0, tension=1 ):

    if len(motion_list[0]) <= 4:
        padMotion(motion_list)
      
    
    #--- Refer algorithm to py_test8_modify_all_frames_parameterized.py
 
    m = []
    m_temp = []
    m_all = []
    ch = 1
    
    for point in motion_list:
	
        for index in range(len(point)-3):
            for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]:
  	        p = interp(point[index], point[index+1], point[index+2], point[index+3], mu, bias, tension)

	        p = abs(int(p))
		m_temp.append(p)

	    m.extend(m_temp)
	    m_temp = []

	    if index == len(point)-4:
                for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]:
  	            p = interp(point[index], point[index+1], point[index+2], point[index+3], mu, bias, tension)
			
		    p = abs(int(p))
		    m_temp.append(p)
		    
	        m.extend(m_temp)
		
	        m_temp = []

	m_all.append(m)
	
	m = []
	
	ch+=1 #--- counter to keep track of channel number
    
    return m_all

def padMotion(data):
    #--- Pad the list if the motion length is <= 4
    #--- Note: 'data' must be a 2-D list

    for d in data:
        while len(d) <= 4:	
	    d.insert(0, d[0])
	    d.insert(len(d), d[len(d)-1])

   

#==== CONVOLUTION (Multiresolution filtering) ===

def multiresFiltering(data):

    #--- Note: data must be a 2-D list
    #--- this multiresfilter initialization must be moved to __init__ if this is turned into an object
    filt = multiresfilter.kfilter(len(data[0]))

    filtered = []
    filtered = filt.filterAll(data)
       
    return filtered
    

#==== from Fusion modules - currently unused ===

def DecTohex(decList):
    pass 

""" =========================================
    Test:
	- read KHR-1 .csv motion file
	- interpolate the points
	- apply multiresolution filtering to the interpolated points    

    Modules:
	- KHR1readcsv:	read .csv motion file, and format it into a 2-D tuple: a list of KHR-1 channels, and each element is a list of motion for the channel
	- interpolation: interpolate points
        - multiresfilter: multiresolution filtering

    =========================================
"""

mo_list = []
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/somersault.csv")
mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv")


rs = interpolate(mo_list)
filtered = []
filtered = multiresFiltering(rs)

i=0
j=0

for freq in filtered:
    print "Frequency bands for Channel ",i," :"
    for fbd in freq:
        print "CH:",i,", FB_",j," = ", fbd
        j += 1
    j = 0
    i += 1

#writer = csv.writer(open("test_convolved_data.csv", "wb"))

#for rows in filtered:
#    writer.writerows(rows)

