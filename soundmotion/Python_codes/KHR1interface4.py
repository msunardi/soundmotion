import sys

sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")
sys.path.append("/home/msunardi/Desktop/Downloads/Fusion-0.10.2/Fusion/Utils")

import KHR1Serial_test as KHR1Serial
import PyDebug
import threading

class khr1Interface (threading.Thread):

    def __init__(self, device, data=None):
        threading.Thread.__init__ (self)
        self.db = PyDebug.PyDebug('KHR1Serial', debuglevel=5)
        self.serial = KHR1Serial.KHR1Serial(dbgobj=None)
        self.serial.Open(device)
        self.speed = 0x05
        self.data = data
        self.home0 = [0xee, 0x00, 0x00]
        self.home1 = [0xee, 0x01, 0x00]

    def run(self):
        print "Running thread...",
        #threading.Thread(target=self.runMe(data)).start()
        if type(self.data).__name__ == 'list':
            self.runMe(self.data)
        elif type(self.data).__name__ == 'int':
            self.runMotion(self.data)
        elif type(self.data).__name__ == 'str':
            self.runScenario(self.data)
        else:
            print "I don't know what you're trying to do, but I don't like it."
        #self.runHome()
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

            print "Out (float): ", li[0:12]
            print "Out (int): ", l[3:len(l)]
            self.serial.SendCmd(l,2, 'ack')
        print "Data sent."

    def runMotion(self, data):
        print "Running motion #:", data
        l = [0xef, 0x00, data]
        if self.serial.SendCmd(l, 2, 'ack'):
            m = [0xef, 0x01, data]
            if self.serial.SendCmd(m, 2, 'ack'):
                print "Motion successfully executed."
                #if self.serial.SendCmd(self.home0, 2, 'ack'):
                #    self.serial.SendCmd(self.home1, 2, 'ack')

        else:
            print "There were some problems..."

    def runScenario(self, command):
        print "Running scenario...", command
        if command == 'dance':
            l = [0xee, 0x00, 0x01]
            if self.serial.SendCmd(l, 2, 'ack'):
                m = [0xee, 0x01, 0x01]
                self.serial.SendCmd(m, 2, 'ack')
        if command == 'home':
            if self.serial.SendCmd(self.home0, 2, 'ack'):
                self.serial.SendCmd(self.home1, 2, 'ack')

    def runHome(self):
        if self.serial.SendCmd(self.home0, 2, 'ack'):
            self.serial.SendCmd(self.home1, 2, 'ack')

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
