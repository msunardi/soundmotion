""" ==================================
    Using Fusion's KHR1 interface to send/read data

    ==================================
"""

import KHR1readcsv
import serial
import sys
sys.path.append("/home/msunardi/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Downlaods/Fusion-0.10.2/Fusion/Utils")
import KHR1Serial_test as KHR1Serial
import PyDebug as PyDebug

"""if __debug__:
    dbg = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
else:
    dbg = None
"""
khr1ser = KHR1Serial.KHR1Serial(dbgobj=None)
khr1ser.Open("/dev/ttyUSB0")
rsp = khr1ser.SendCmd([0xfd, 0x01, 0x03]+[45]*12, 2, 'ack')

