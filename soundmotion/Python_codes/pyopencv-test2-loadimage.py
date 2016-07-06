import sys
sys.path.append("/home/msunardi/opencv/1.1.0/lib/python2.5/gb-cvtypes")

from CVtypes2 import cv


win = "load image"
cv.NamedWindow(win)
img = cv.LoadImage("/home/msunardi/opencv/1.1.0/share/opencv/samples/c/lena.jpg")
#img = cv.LoadImage("/home/msunardi/Python-project/imagex.jpg")
while cv.WaitKey(1) is not 27:
    cv.ShowImage(win, img)
