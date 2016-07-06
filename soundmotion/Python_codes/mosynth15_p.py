""" ---------------------------------------------------
        mosynth14_p.py (derived from mosynth12_p.py) - 4/20/09

        Function:
        - (re) read KHR-1 motion from .csv file
        - (in) does interpolation of the motion
        - (cv) does multiresolution filtering of the interpolated motion
        - concatenate motions

        Modules:
        - KHR1readcsv:	read .csv motion file, and format it into a 2-D tuple: a list of KHR-1 channels, and each element is a list of motion for the channel
        - interpolation: interpolate points
        - multiresfilter4: multiresolution filtering with gain retrieval
        - emote:
        - qwt_test1: plotter

    ---------------------------------------------------
"""


import KHR1readcsv as motion
import KHR1_motionrange2 as khr1range
import interpolation
import multiresfilter4 as mrf
import csv
import emote
import plotter
import sys
import numpy
#from qt import *
from PyQt4 import Qt

sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")
import KHR1Serial_test as KHR1Serial
import PyDebug


class MotionSynthesizer:

    def __init__(self):
        self.gains = []
        self.DATA = []
        self.emote_parameters = {"weight": 0, "time": 0, "space": 0, "flow": 0}
        #self.interp = interpolation.hermiteInterpolate
        self.interp = interpolation.kbInterpolate
        #self.filt = multiresfilter4.kfilter(len(data[0]))
        pass

    #=== READ CSV ===
    """    
        when read, returns an list of lists (2-D list).
            The list is organized so each element of the list (which is also a list) is the motion of a channel/servo
    """
    def readCSV( self, path ):
        return motion.read(path)

    #=== INTERPOLATION  ===
    def interpolate( self, motion_list, bias=0, tension=0, continuity=0 ):
        #self.interp = interpolation.hermiteInterpolate

        if len(motion_list[0]) <= 4:
            motion_list = self.padMotion(motion_list)
        
        #--- Refer algorithm to py_test8_modify_all_frames_parameterized.py
 
        self.m = []
        self.m_temp = []
        self.m_all = []
        self.ch = 1
    
        for point in motion_list:   #--- for each channel...
        
            for index in range(len(point)-3):   #--- for each data point in the channel...
                for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
                    self.p = self.interp(point[index], point[index+1], point[index+2], point[index+3], mu, tension, bias, continuity)

                    self.p = abs(int(self.p))
                    self.m_temp.append(self.p)

                self.m.extend(self.m_temp)

                self.m_temp = []

                if index == len(point)-4:
                    for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
                        self.p = self.interp(point[index+1], point[index+3], point[index+3], point[index+3], mu, tension, bias, continuity)
                        
                        self.p = abs(int(self.p))
                        self.m_temp.append(self.p)
                    self.m_temp.append(self.interp(point[index+1], point[index+2], point[index+3], point[index+3], 1, tension, bias, continuity))
                    self.m.extend(self.m_temp)
                
                    self.m_temp = []

            self.m_all.append(self.m)
        
            self.m = []
        
            self.ch+=1 #--- counter to keep track of channel number
    
        return self.m_all

    def padMotion(self, data):
        #--- Pad the list if the motion length is <= 4
        #--- Note: 'data' must be a 2-D list

        print "Data = ", data
        

        for d in data:            
            while len(d) <= 4:
                d.insert(0, d[0])
                d.insert(len(d), d[len(d)-1])
                #numpy.put(d, 0, d[0])
                #numpy.put(d, len(d)-1, d[len(d)-1])
                #try:
                #    d.insert(0, d[0])
                #    d.insert(len(d), d[len(d)-1])
                #except:
                #    numpy.put(d, 0, d[0])
                #    numpy.put(d, len(d)-1, d[len(d)-1])
                #    print "D = ", d, type(d)
        print "new Data = ", data
        return data

    def interpolate2(self, data):
        tension = 0
        bias = 0
        self.d = []
        self.d_temp = []
        print "data = ", data
        
        for index in range(len(data)-3):
            for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
                self.p = self.interp(data[index], data[index+1], data[index+2], data[index+3], mu, tension, bias)

                #self.p = abs(int(self.p))
                self.p = float(self.p)
                self.d_temp.append(self.p)

            self.d.extend(self.d_temp)

            self.d_temp = []

            if index == len(data)-4:
                for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
                    self.p = self.interp(data[index+1], data[index+3], data[index+3], data[index+3], mu, tension, bias)
                        
                    #self.p = abs(int(self.p))
                    self.p = float(self.p)
                    self.d_temp.append(self.p)
                self.d_temp.extend(float(self.interp(data[index+1], data[index+2], data[index+3], data[index+3], 1, tension, bias)))
                self.d.extend(self.d_temp)
                
                self.d_temp = []

        return self.d    

    def interpolate3(self, motion_list, int_rate=None, bias=0, tension=0):
        if int_rate == 2:
            rate = [0, .5]
        elif int_rate == 3:
            rate = [0, .25, .5, .75]
        else:
            rate = [0, .125, .25, .375, .5, .625, .75, .875]

        if len(motion_list[0]) <= 4:
            motion_list = self.padMotion(motion_list)
            
        #tension = 0
        #bias = 0
        self.x = []
        self.x_temp = []
        self.x_all = []
        print "data = ", motion_list
        for data in motion_list:
            for index in range(len(data)-3):
                for mu in rate:
                    self.w = self.interp(data[index], data[index+1], data[index+2], data[index+3], mu, tension, bias)

                    #self.p = abs(int(self.p))
                    self.x_temp.append(self.w)
                self.x.extend(self.x_temp)

                self.x_temp = []

                if index == len(data)-4:
                    for mu in rate:
                        self.w = self.interp(data[index+1], data[index+3], data[index+3], data[index+3], mu, tension, bias)
                        
                        #self.p = abs(int(self.p))
                        self.x_temp.append(self.w)
                    self.x_temp.append(self.interp(data[index+1], data[index+2], data[index+3], data[index+3], 1, tension, bias))
                    self.x.extend(self.x_temp)
                
                    self.x_temp = []

            self.x_all.append(self.x)
        
            self.x = []


        return self.x_all

    #=== SYNTHESIZE MOTION
    def concatenatemotion(self, motion1, motion2):
        concat = numpy.concatenate((motion1, motion2), 1)
        concat = list(concat)
        for i in enumerate(concat):
            concat[i[0]] = list(i[1])
        
        print "type concat: ", type(concat)
        return concat
    
    #=== MULTIRESOLUTION FILTERING ===

    def multiresFiltering(self, data=None):

        #--- Note: data must be a 2-D list
        #--- this multiresfilter initialization must be moved to __init__ if this is turned into an object
        if data is None:
            data = self.DATA
            print "filtering with internal DATA..."
        else:
            self.DATA = data
            print "filtering with external data..."
        self.filt = mrf.kfilter(len(data[0]))

        self.filtered = []
        self.filtered = self.filt.filterAll(data)
        self.gains = []
        self.gains = self.filt.getGains(self.filt.filterAll(data))
       
        #return filtered
        return self.gains

    def adjustGain(self, channel, band, adjustment):
        self.gains[channel][band:band+1] = [self.filt.adjustGain(self.gains, channel, band, adjustment)]

    def returnNewData(self):
        return self.filt.getOriginalData(self.filtered, self.gains)

    def getNewSingleChannelData(self, channel):
        return self.filt.getIndividualData(self.filtered[channel], self.gains[channel])

    def mrfDoItAll(self, data, CH=0, G=0, x=0):
        self.filt = mrf.kfilter(len(data[0]))
        #G = 0      # Tests: 0 - 5
        #w = 1.5    # Tests: 1.5
        
        #x = self.filt.doItAll(data, 0, G, w)
        x = self.filt.doItAll(data, CH, G, x)
        #x = self.filt.doItAll(data, 5, 4, 2)
        #x = self.filt.doItAll(x, 5, 3, 2)
        #=========================ch^,G^,w^ (ch = channel, G = band, w = Gain)
        
        #=== Apply to multiple channels at once
        #for m in range(11,23,1):
            #x = self.filt.doItAll(x, m+1, G, w)
            
            #=== used in mosynth4_0.csv, mosynth5_1_walk.csv
            #x = self.filt.doItAll(x, m+1, 2, 1.5)
            #x = self.filt.doItAll(x, m+1, 3, 2)
            #x = self.filt.doItAll(x, m+1, 4, 2.5)

            #=== used in mosynth4_1.csv, mosynth5_2_walk.csv
            #x = self.filt.doItAll(x, m+1, 2, -1.5)
            #x = self.filt.doItAll(x, m+1, 3, -2)
            #x = self.filt.doItAll(x, m+1, 4, -2.5)

            #=== used in mosynth5_3_walk.csv
            #x = self.filt.doItAll(x, m+1, 0, 3)
            #x = self.filt.doItAll(x, m+1, 1, 2)
            #x = self.filt.doItAll(x, m+1, 2, 1.5)

            #=== used in mosynth5_4_walk.csv
            #x = self.filt.doItAll(x, m+1, 0, -2)
            #x = self.filt.doItAll(x, m+1, 1, -1.5)
            #x = self.filt.doItAll(x, m+1, 2, 1)
            #x = self.filt.doItAll(x, m+1, 3, 1.5)
            #x = self.filt.doItAll(x, m+1, 4, 2.5)
            #x = self.filt.doItAll(x, m+1, 5, 2)

            #=== used in mosynth5_5_walk.csv
            #x = self.filt.doItAll(x, m+1, 0, -2)
            #x = self.filt.doItAll(x, m+1, 1, -1.5)
            #x = self.filt.doItAll(x, m+1, 2, 1)
            #x = self.filt.doItAll(x, m+1, 3, 1.5)
            #x = self.filt.doItAll(x, m+1, 4, 2.5)
            #x = self.filt.doItAll(x, m+1, 5, 2)


        return x
        #return self.filt.doItAll(data, 1, 5, 2)

    #==== from Fusion modules - currently unused ===

    def DecTohex(self, decList):
        pass 

    #=== EMOTE MODEL ===

    def emoting(self, weight, time, space, flow, e_angle):
        self.E = emote.efforts(weight, time, space, flow)
        self.in_ti = emote.ti(E)
        self.in_v0 = emote.v0(E)
        self.in_v1 = emote.v1(E)
        self.in_texp = emote.texp(E)
        self.in_elbow_angle = emote.elbow_angle(E, e_angle) #e_angle = elbow angle
        self.in_vt__ = emote.vt__(0.5, self.in_ti, self.in_v0, self.in_v1, self.in_texp) # replace 0.5 with v_ (acceleration)

        #print "ti= ", self.in_ti,"| v0= ", self.in_v0, "| v1= ", self.in_v1, "| texp= ", self.in_texp
        #print "elbow_angle= ", self_in_elbow_angle, "| vt__= ", self.in_vt__

    #=== DRAWING/PLOTTING method ===
    def goShow(self, data, param):
        pass

    def read(self, path):
        return motion.read(path)

    def countGains(self):
        return len(self.gains[0])


    #=== NORMALIZE SIGNAL ===
    """
        signals need to be normalized so they don't go beyond the byte or joint angle limit
    """
    def returnNormalized(self):
        """ data is arranged as:
            dimension 1: channels 1 - 24 (index: 0 - 23)
            dimension 2: joint angle over time (length depends on movement)
        """
        #data = self.filt.getOriginalData(self.filtered, self.gains)
        data = self.DATA
        #print "data 24: ", data[23]
        #print "range: ", khr1range.KHR1motionrange2[0]

        for d in range(len(data)):
           print "Channel ",d+1," range: ", khr1range.KHR1motionrange2[d]
                
        
""" =========================================
    Test:
        - read KHR-1 .csv motion file
        - interpolate the points
        - apply multiresolution filtering to the interpolated points    

    Modules:
        - KHR1readcsv:	read .csv motion file, and format it into a 2-D list: a list of KHR-1 channels, and each element is a list of motion for the channel
        - interpolation: interpolate points
        - multiresfilter: multiresolution filtering

    =========================================
"""

# --- last changed: 2/1/09
ms = MotionSynthesizer()

#=== 1. Read motion file
# --- last changed: 2/1/09 mo_list = []
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/somersault.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/gait_back_roll.csv")
# --- last changed: 2/1/09 mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/better_fwd_walk_data.csv")

"""
mo_list = ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_cocky.csv")
mo_list2 = ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_relax.csv")
mo_list3 = ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_bird.csv")
mo_list4 = ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_left.csv")
mo_list5 = ms.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH7.csv")
#=== 2. Interpolate motion list >>> moved to last
#rs = ms.interpolate3(mo_list, 3)
#print "RS = ", rs, "length: ", len(rs)
#rs2 = ms.interpolate3(mo_list2, 3)
#print "RS2 = ", rs2, "length: ", len(rs2)
#print "molist", mo_list
#print "molist2", mo_list2
#print "molist3", mo_list3
#rsx = ms.concatenatemotion(mo_list2, mo_list3)
#--- CONCATENATION DEMO
rsx = ms.concatenatemotion(ms.concatenatemotion(ms.concatenatemotion(ms.concatenatemotion(ms.concatenatemotion(ms.concatenatemotion(ms.concatenatemotion(mo_list5, mo_list), mo_list2), mo_list2), mo_list2), mo_list3), mo_list4), mo_list5) 
print "RSX = ", rsx, type(rsx[0])
#rs = ms.interpolate3(rsx, 5, 0, 2)
rs = ms.interpolate(rsx)
#print "interpolated rsx = ", rs
                                 
#for r in zip(*rs):
#    print r
#=== 3. Apply multiresolution filtering
#filtered = []

#=== 3.a. Extract low pass sequence by filtering (convolving with kernel)
#filtered = ms.multiresFiltering(rs)
#filtered = ms.multiresFiltering(mo_list)

#i=0
#j=0
"""
#=== 3.b. Extract bandpass filter bands
"""for freq in filtered:
    print "Gains for Channel ",i," :"
    for fbd in freq:
        print "CH:",i,", L_",j," = ", fbd
        j += 1
    j = 0
    i += 1
"""
#writer = csv.writer(open("test_convolved_data.csv", "wb"))

#for rows in filtered:
#    writer.writerows(rows)

#=== 3.c. Does step 3.a. and 3.b. all in one (i.e. makes step 3.a. and 3.b. only for showing what is being done)

#new_rs = ms.mrfDoItAll(rs)

# --- last changed: 2/1/09 new_rs = ms.mrfDoItAll(mo_list)
#print "New motion data: ", new_rs

#=== 3.d. Interpolate results
# --- last changed: 2/1/09 rx = ms.interpolate(new_rs)

#=== 4. PRINT OUT RESULTS

#for i in (zip(*new_rs)):
#    print i

# --- last changed: 2/1/09
"""
print "Original data:"
for k in (zip(*mo_list)):
    print k

print "New interpolated data:"
for i in (zip(*rx)):
    print i
"""

#servo1=new_rs[0]
#servo2=new_rs[1]
#data = zip(*rx)[5]
"""app = Qt.QApplication(sys.argv)
demo = plotter.MyPlot()
for data in rx:
    demo.addCurve(data)
#demo.plotData(servo1)
#demo.plotData(servo2)
#demo.addData(servo1, servo2)
#demo.plotData()
#app.setMainWidget(demo)
demo.resize(400,400)
demo.show()
app.exec_()


#=== 5. WRITE TO SERIAL PORT (to KHR-1)

db = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
khr1ser = KHR1Serial.KHR1Serial(dbgobj=None)
khr1ser.Open("/dev/ttyUSB1")

for li in zip(*rs):
    l = [0xfd, 0x00, 0x05]
    
    for lo in li[0:12]:
        loi = int(lo)
        if loi < 0:
            loi = 0
        if loi > 255:
            loi = 255
        l+=[loi]
    #print li[0:12]
    khr1ser.SendCmd(l, 2, 'ack')

    #while not khr1ser.SendCmd(l, 2, 'ack'):
    #    print "..."
   
    #exit()


new_rs = zip(*new_rs)
for li in new_rs:
    l = [0xfd, 0x00, 0x05]
    
    for lo in li[0:12]:
        l+=[int(lo)]
    #print li[0:12]

    khr1ser.SendCmd(l, 2, 'ack')
"""
