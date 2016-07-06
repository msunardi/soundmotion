import serial

ser = serial.Serial("/dev/ttyUSB0", 115200)

print ser

ser.open()

print ser.portstr, ser.isOpen()

if ser.isOpen():
    ser.write("hellooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")

ser.close()

print "serial is closed"
