import sys
sys.path.append("/home/msunardi/opencv/1.1.0/lib/python2.5/gb-cvtypes/")

from CVtypes2 import cv

def detect(image):
    #print "image size..."
    image_size = cv.GetSize(image)
    #print "grayscale..."
    grayscale = cv.CreateImage(image_size, 8, 1)
    #print "cvtcolor..."
    cv.CvtColor(image, grayscale, 7)
    #cv.Copy(image, grayscale)
    #print "creating memstorage..."
    storage = cv.CreateMemStorage(0)
    cv.ClearMemStorage(storage)
    #print "memstorage created!"

    cv.EqualizeHist(grayscale, grayscale)

    cascade = cv.LoadHaarClassifierCascade('/home/msunardi/opencv/1.1.0/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml', cv.Size(1,1))
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, cv.HAAR_DO_CANNY_PRUNING, cv.Size(50,50))
    #faces = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.HAAR_DO_CANNY_PRUNING, cv.Size(50,50))

    if faces:
        print '%d face detected!' % len(faces)
        sys.stdout.flush()
        
        for i in faces:
            cv.Rectangle(image, cv.Point( int(i.x), int(i.y)),
                         cv.Point(int(i.x + i.width), int(i.y + i.height)),
                         cv.RGB(0, 255, 0), 3, 8, 0)
                         

if __name__ == "__main__":
    print "OpenCV version: %s (%d, %d, %d)" % (cv.VERSION, cv.MAJOR_VERSION, cv.MINOR_VERSION,cv.SUBMINOR_VERSION)

    print "Press ESC to exit ..."

    cv.NamedWindow('Camera', cv.WINDOW_AUTOSIZE)
    device = 0
    capture = cv.CreateCameraCapture(0)
    cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_WIDTH, 640)
    cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_HEIGHT, 480)

    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    while 1:

        frame = cv.QueryFrame(capture)
        if frame is None:
            break

        #cv.Flip(frame, None, 1)
        detect(frame)
        cv.ShowImage('Camera', frame)
        k = cv.WaitKey(10)
   
        if k == 0x1b:
            print "ESC pressed. Exiting ..."
            break
