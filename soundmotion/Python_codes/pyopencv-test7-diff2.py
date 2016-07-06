import opencv as cv
import opencv.highgui as hg
import numpy
import opencv.adaptors as cvadaptor
import sys

def detect_and_draw(image):
    image_size = hg.cvGetSize(image)
    grayscale = cv.cvCreateImage(image_size, 8, 1)
    cv.cvCvtColor(image, grayscale, CV_RGB2GRAY)
    return grayscale

if __name__=="__main__":
    hg.cvNamedWindow('capture', hg.CV_WINDOW_AUTOSIZE)
    capture = hg.cvCreateCameraCapture(0)
    
    if not capture:
        print "Error opening capture device..."
        sys.exit(1)

    while True:
        frame = hg.cvQueryFrame(capture)
        if frame is None:
            break

        hg.cvShowImage('capture', frame)
        k = hg.cvWaitKey(10)

        if k == 0x1b:
            print "ESC pressed.  Exiting..."
            break
    
