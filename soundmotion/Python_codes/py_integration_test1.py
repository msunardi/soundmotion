import KHR1readcsv
import serial
import sys
sys.path.append("/home/msunardi/Downloads/Fusion-0.10.2/Fusion/KHR1/Cmd")

def writeout():

    l = []
    out = ''
    ser = serial.Serial("/dev/ttyUSB0", 115200)
    
    l = KHR1readcsv.read("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv")

    ser.open()

    if ser.isOpen():
        for x in l[0]:
            out += (str(x))

        print out
        ser.write(out)

    ser.close()

writeout()
