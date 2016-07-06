import KHR1readcsv as motion
import interpolation
import sys
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")
import KHR1Serial_test as KHR1Serial
import PyDebug as PyDebug
import random
import multiresfilter
import bandpassbands
import csv


class KHR1MotionSignal:

    def __init__(self, mo_list):
        self.motion_list = []
        # If there are more than 4 (key) positions in the motion..
        # ... do Hermite interpolation normally
        if len(mo_list[0]) <= 4:
            """ Otherwise, need to add positions in the beginning and the end of the motion
                the added positions in the beginning and the end is the same as start and end
                positions, respectively
            """
            for mo in mo_list:
                mo_length = len(mo)
                mo.insert(0, mo[0])
                mo.insert(mo_length, mo[mo_length])
    
        for i in range(len(mo_list)):
            self.motion_list.append(mo_list[i][:])

        self.interpH = interpolation.hermiteInterpolate
        self.bpb = bandpassbands.bandPassBands()
        #self.mrf = multiresfilter.kfilter(self.motion_list) # must provide motion list as parameter


    def interpolate(self, motion_list, bias=0, tension=0 ):
    # Refer algorithm to py_test8_modify_all_frames_parameterized.py
 
        m = []
        m_temp = []
        m_all = []
        ch = 1
    
        for point in motion_list:
    
            for index in range(len(point)-3):
                for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]:
                    p = self.interpH(point[index], point[index+1], point[index+2], point[index+3], mu, bias, tension)

                    p = abs(int(p))
                m_temp.append(p)

            m.extend(m_temp)
            m_temp = []

            if index == len(point)-4:
                for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]:
                    p = self.interpH(point[index], point[index+1], point[index+2], point[index+3], mu, bias, tension)
            
                    p = abs(int(p))
                m_temp.append(p)
            
                m.extend(m_temp)
        
                m_temp = []

            m_all.append(m)
    
        m = []
    
        ch+=1 # Counter to keep track of channel number
    
        return m_all

    def filterData(self, motion_data):
        self.mrf = multiresfilter.kfilter(motion_data) # must provide motion list as parameter

        return self.mrf.filterAll(motion_data)

    def returnBandsData(self, filtered_data):
        return self.bpb.bringItOn(filtered_data)


""" =========================================
    Test:
    - read KHR-1 .csv motion file
    - interpolate the points
    - ready the interpolated motion (in RCB-1 word format) for serial out    Components:
    - KHR1readcsv:  read .csv motion file, and format it into a 2-D tuple: a list of KHR-1 channels, and each element is a list of motion for the channel
    - interpolation: interpolate points
    - filter: apply filtering to interpolated motion and get frequency bands for each channel
    - bandpass: find bandpass for each frequency bands

    =========================================
"""

mo_list = []
mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/somersault.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv")

kms = KHR1MotionSignal(mo_list)

print kms.returnBandsData(kms.filterData(kms.interpolate(mo_list)))

"""writer = csv.writer(open("test_convolved_data.csv", "wb"))

for rows in filtered:
    writer.writerows(rows)
"""
