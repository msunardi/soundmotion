import sys
sys.path.append("/home/msunardi/opencv/1.1.0/lib/python2.5/gb-cvtypes")

#from CVtypes import cv
from CVtypes2 import cv

cv.NamedWindow("win")
img = cv.LoadImage("/home/msunardi/opencv/1.1.0/share/opencv/samples/c/box.png")

while cv.WaitKey(1) is not 27:
    cv.ShowImage("win", img)
