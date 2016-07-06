import sys

sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")

import KHR1Serial_test as KHR1Serial
import PyDebug
import threading

class khr1Interface:

    def __init__(self, device):
        self.db = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
        self.serial = KHR1Serial.KHR1Serial(dbgobj=None)
        self.serial.Open(device)
        self.speed = 0x05

    def run(self, data):
        print "Running thread...",
        threading.Thread(target=self.runMe(data)).start()
        print "thread is running"

    def runMe(self, data):
        print "Sending data..."
        for li in zip(*data):
            l = [0xfd, 0x00, self.speed]

            for lo in li[0:12]:
                if lo < 0:
                    l+=[0x00]
                elif (lo-int(lo)) < 0.5:
                    l+=[int(lo)]
                else:
                    l+=[int(lo)+1]

            print "Out (float): ", li[0:12]
            print "Out (int): ", l[3:len(l)]
            self.serial.SendCmd(l,2, 'ack')
        print "Data sent."

    def setSpeed(self, speed):
        print "Old speed: ", self.speed
        print "New speed: ", speed
        self.speed = speed
