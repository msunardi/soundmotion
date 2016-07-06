import sys
sys.path.append("/home/msunardi/opencv/1.1.0/lib/python2.5/gb-cvtypes")

from CVtypes2 import cv

win = 'show cam'
cv.NamedWindow(win)
cap = cv.CreateCameraCapture(0)
while cv.WaitKey(1) != 27:
    img = cv.QueryFrame(cap)
    cv.ShowImage(win, img)

