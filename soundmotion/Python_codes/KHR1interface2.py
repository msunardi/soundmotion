import sys

sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")

import KHR1Serial_test as KHR1Serial
import PyDebug
import threading

class khr1Interface (threading.Thread):

    def __init__(self, device, data):
        threading.Thread.__init__ (self)
        self.db = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
        self.serial = KHR1Serial.KHR1Serial(dbgobj=None)
        self.serial.Open(device)
        self.speed = 0x05
        self.data = data

    def run(self):
        print "Running thread...",
        #threading.Thread(target=self.runMe(data)).start()
        self.runMe(self.data)
        print "thread is done."

    def runMe(self, data):
        print "Sending data..."
        for li in zip(*data):
            l = [0xfd, 0x00, self.speed]

            for lo in li[0:12]:
                """if lo < 0:
                    l+=[0x00]
                elif abs(lo-int(lo)) < 0.5:
                    l+=[int(lo)]
                else:
                    l+=[int(lo)+1]
                """
                l += [self.cap(lo)]

            #print "Out (float): ", li[0:12]
            print "Out (int): ", l[3:len(l)]
            self.serial.SendCmd(l,2, 'ack')
        print "Data sent."

    def cap(self, point):
        if point < 0:
            return 0x00
        elif abs(point-int(point)) < 0.5:
            a = int(point)
        else:
            a = int(point)+1
        if a >= 180 and a != 225:
            return 0xb4
        else:
            return a

    def setSpeed(self, speed):
        print "Old speed: ", self.speed
        print "New speed: ", speed
        self.speed = speed
