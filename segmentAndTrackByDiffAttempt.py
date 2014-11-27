# filterBlue.py
# Taylor Brockhoeft
#
# This program attempts to segment, and then track, swimmers in a pool.
# Current Status: not working

# Using Differental Images to detect motion
#

import cv2
import numpy as np

#Global Constants
MHI_DURATION = 0.5
DEFAULT_THRESHOLD = 32
MAX_TIME_DELTA = 0.25
MIN_TIME_DELTA = 0.05


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

def nothing(*arg, **kw):
    """Null Function for trackbar"""
    pass

def draw_motion_comp(vis, (x, y, w, h), angle, color):
    """Visually isolates where movement is occuring"""
    cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 0))
    r = min(w/2, h/2)
    cx, cy = x+w/2, y+h/2
    angle = angle*np.pi/180
    cv2.circle(vis, (cx, cy), r, color, 3)
    cv2.line(vis, (cx, cy), (int(cx+np.cos(angle)*r), int(cy+np.sin(angle)*r)), color, 3)

def crop(frame):
    """Crops an Image""" 
    return frame[100:100, 100:100]


def segment(frame):
    """This Function Segments Swimmers from the image, and returns the same frame after the mask"""
    #Blur
    kernel = np.ones((5,5),np.uint8)
    finekernel = np.ones((3,3),np.uint8)
    # define range of blue color in HSV
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([130,255,255])

    # Convert BGR to HSV
    hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    imgMask = cv2.inRange(hsvimg, lower_blue, upper_blue)

    #morphological opening (removes small objects from the foreground)
    #Erode and Expand the edges of the mask to eliminate small artifacts
    imgMask = cv2.erode(imgMask, kernel, iterations=1)
    imgMask = cv2.dilate(imgMask, kernel, iterations=1)

    #morphological closing
    #Erode and Expand the edges to smooth edges
    imgMask = cv2.dilate(imgMask, kernel, iterations=1)
    imgMask = cv2.erode(imgMask, kernel, iterations=1)

    #InvertMask
    imgMask = cv2.bitwise_not(imgMask,imgMask)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= imgMask)

    return res


#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('MVI_7026.mp4')

ret, frame = cap.read()

#frame = segment(frame)

t_prev = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
t_current = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
t_next = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

count = 0 
while(1):
    count = count+1
    if(count%1==0):
        cv2.imshow( "result", diffImg(t_prev, t_current, t_next)*20 )

        # Take each frame
        ret, frame = cap.read()
        #frame = segment(frame)

        # Read next image
        t_prev = t_current
        t_current = t_next
        t_next = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()