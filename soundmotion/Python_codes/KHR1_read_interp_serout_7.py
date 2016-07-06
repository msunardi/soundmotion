import KHR1readcsv as motion
import interpolation
import sys
sys.path.append("/home/msunardi/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Downloads/Fusion-0.10.2/Fusion/Utils")
import KHR1Serial_test as KHR1Serial
import PyDebug as PyDebug
import random

interp = interpolation.hermiteInterpolate

def interpolate( motion_list, bias=0, tension=1 ):

#   Refer algorithm to py_test8_modify_all_frames_parameterized.py
 
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
	
	ch+=1 #counter to keep track of channel number
    
    return m_all

def DecTohex(decList):
    pass 

""" =========================================
    Test:
	- read KHR-1 .csv motion file
	- interpolate the points
	- ready the interpolated motion (in RCB-1 word format) for serial out    Components:
	- KHR1readcsv:	read .csv motion file, and format it into a 2-D tuple: a list of KHR-1 channels, and each element is a list of motion for the channel
	- interpolation: interpolate points

    =========================================
"""

mo_list = []
mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/somersault.csv")
#mo_list = motion.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv")

print mo_list

#readySerial = []
#rs = zip(*interpolate(mo_list))
#print len(mo_list)

# If there are more than 4 (key) positions in the motion..
# ... do Hermite interpolation normally
if len(mo_list[0]) > 4:
    rs = interpolate(mo_list)

else:
    """ Otherwise, need to add positions in the beginning and the end of the motion
        the added positions in the beginning and the end is the same as start and end
        positions, respectively
    """
    for mo in mo_list:
	mo_length = len(mo)
	mo.insert(0, mo[0])
	mo.insert(mo_length, mo[mo_length])
    
    rs = interpolate(mo_list)

print rs[0]

rs = zip(*rs)
print rs
#print readySerial


db = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
#khr1ser = KHR1Serial.KHR1Serial(dbgobj=db)
khr1ser = KHR1Serial.KHR1Serial(dbgobj=None)
khr1ser.Open("/dev/ttyUSB0")


for li in rs:
  
    l = [0xfd, 0x00, 0x05]
  
    for lo in li[0:12]:
        #print lo
        l += [lo]
    print li[0:12]
  
    khr1ser.SendCmd(l, 2, 'ack')
    
  
