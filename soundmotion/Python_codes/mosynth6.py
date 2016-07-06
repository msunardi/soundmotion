""" ---------------------------------------------------
        mosynth5.py (derived from mosynth4.py)

        Function:
        - (re) read KHR-1 motion from .csv file
        - (in) does interpolation of the motion
        - (cv) does multiresolution filtering of the interpolated motion

        Modules:
        - KHR1readcsv:	read .csv motion file, and format it into a 2-D tuple: a list of KHR-1 channels, and each element is a list of motion for the channel
        - interpolation: interpolate points
        - multiresfilter2: multiresolution filtering with gain retrieval
        - emote:
        - qwt_test1: plotter

    ---------------------------------------------------
"""


import KHR1readcsv as motion
import interpolation
import multiresfilter3
import csv
import emote
import qwt_plotter
import sys

from qt import *

sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")
import KHR1Serial_test as KHR1Serial
import PyDebug


class MotionSynthesizer:

    def __init__(self):
        
        pass

    #=== READ CSV ===
    """    
        when read, returns an list of lists (2-D list).
            The list is organized so each element of the list (which is also a list) is the motion of a channel/servo
    """
    def readCSV( self, path ):
        return motion.read(path)

    #=== INTERPOLATION  ===
    def interpolate( self, motion_list, bias=0, tension=1 ):
        self.interp = interpolation.hermiteInterpolate

        if len(motion_list[0]) <= 4:
            self.padMotion(motion_list)
        
        #--- Refer algorithm to py_test8_modify_all_frames_parameterized.py
 
        self.m = []
        self.m_temp = []
        self.m_all = []
        self.ch = 1
    
        for point in motion_list:
        
            for index in range(len(point)-3):
                for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]:
                    self.p = self.interp(point[index], point[index+1], point[index+2], point[index+3], mu, bias, tension)

                    self.p = abs(int(self.p))
                    self.m_temp.append(self.p)

                self.m.extend(self.m_temp)

                self.m_temp = []

                if index == len(point)-4:
                    for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]:
                        self.p = self.interp(point[index], point[index+1], point[index+2], point[index+3], mu, bias, tension)
                        
                        self.p = abs(int(self.p))
                        self.m_temp.append(self.p)
                    
                    self.m.extend(self.m_temp)
                
                    self.m_temp = []

            self.m_all.append(self.m)
        
            self.m = []
        
            self.ch+=1 #--- counter to keep track of channel number
    
        return self.m_all

    def padMotion(self, data):
        #--- Pad the list if the motion length is <= 4
        #--- Note: 'data' must be a 2-D list

        for d in data:
            while len(d) <= 4:	
                d.insert(0, d[0])
                d.insert(len(d), d[len(d)-1])

   

    #=== MULTIRESOLUTION FILTERING ===

    def multiresFiltering(self, data):

        #--- Note: data must be a 2-D list
        #--- this multiresfilter initialization must be moved to __init__ if this is turned into an object
        filt = multiresfilter3.kfilter(len(data[0]))

        #filtered = []
        #filtered = self.filt.filterAll(data)
        self.gains = []
        self.gains = filt.getGains(filt.filterAll(data))
       
        #return filtered
        return self.gains
    

    def mrfDoItAll(self, data):
        self.filt = multiresfilter3.kfilter(len(data[0]))
        #G = 0      # Tests: 0 - 5
        #w = 1.5    # Tests: 1.5
        
        #x = self.filt.doItAll(data, 0, G, w)
        x = self.filt.doItAll(data, 5, 0, -1)
        #x = self.filt.doItAll(data, 5, 4, 2)
        x = self.filt.doItAll(x, 5, 3, 2)
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

ms = MotionSynthesizer()

#=== 1. Read motion file
mo_list = []
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/somersault.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/gait_back_roll.csv")
mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/better_fwd_walk_data.csv")

#mo_list = readCSV("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv")

#=== 2. Interpolate motion list >>> moved to last
#rs = ms.interpolate(mo_list)
#for r in zip(*rs):
#    print r
#=== 3. Apply multiresolution filtering
#filtered = []

#=== 3.a. Extract low pass sequence by filtering (convolving with kernel)
#filtered = ms.multiresFiltering(rs)
#filtered = ms.multiresFiltering(mo_list)

i=0
j=0

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
new_rs = ms.mrfDoItAll(mo_list)
#print "New motion data: ", new_rs

#=== 3.d. Interpolate results
rx = ms.interpolate(new_rs)

#=== 4. PRINT OUT RESULTS

#for i in (zip(*new_rs)):
#    print i
print "Original data:"
for k in (zip(*mo_list)):
    print k

print "New interpolated data:"
for i in (zip(*rx)):
    print i

"""servo1=new_rs[0]
servo2=new_rs[1]
app = QApplication(sys.argv)
demo = qwt_plotter.Demo()
#demo.plotData(servo1)
#demo.plotData(servo2)
demo.addData(servo1, servo2)
demo.plotData()
app.setMainWidget(demo)
demo.resize(400,400)
demo.show()
app.exec_loop()
"""
#=== 5. WRITE TO SERIAL PORT (to KHR-1)
"""
db = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
khr1ser = KHR1Serial.KHR1Serial(dbgobj=None)
khr1ser.Open("/dev/ttyUSB0")

for li in zip(*rs):
    l = [0xfd, 0x00, 0x05]
    
    for lo in li[0:12]:
        l+=[lo]
    #print li[0:12]

    khr1ser.SendCmd(l, 2, 'ack')


new_rs = zip(*new_rs)
for li in new_rs:
    l = [0xfd, 0x00, 0x05]
    
    for lo in li[0:12]:
        l+=[int(lo)]
    #print li[0:12]

    khr1ser.SendCmd(l, 2, 'ack')
"""
