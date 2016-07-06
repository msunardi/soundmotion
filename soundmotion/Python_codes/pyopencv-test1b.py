import sys
sys.path.append("/home/msunardi/opencv/1.1.0/lib/python2.5/gb-cvtypes")

from CVtypes2 import cv


win = 'show cam'
cv.NamedWindow(win, cv.WINDOW_AUTOSIZE)

cap = cv.CreateCameraCapture(0)
cv.SetCaptureProperty(cap, cv.CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(cap, cv.CAP_PROP_FRAME_HEIGHT, 480)

if not cap:
    print "Error opening capture device"
    sys.exit(1)
img = cv.QueryFrame(cap)
while cv.WaitKey(1) != 27:
    #img = cv.QueryFrame(cap)
    #if img is None:
    #    break
    #print "img is not None..."
    cv.ShowImage(win, img)
    img = cv.QueryFrame(cap)
cv.SaveImage("imagex.jpg", img)
