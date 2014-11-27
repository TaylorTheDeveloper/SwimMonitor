# filterBlue.py
# Taylor Brockhoeft
#
# This program attempts to segment swimmers in a pool.
#

import cv2
import numpy as np

def draw_motion_comp(vis, (x, y, w, h), angle, color):
    """Visually isolates where movement is occuring"""
    cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 0))
    r = min(w/2, h/2)
    cx, cy = x+w/2, y+h/2
    angle = angle*np.pi/180
    cv2.circle(vis, (cx, cy), r, color, 3)
    cv2.line(vis, (cx, cy), (int(cx+np.cos(angle)*r), int(cy+np.sin(angle)*r)), color, 3)


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

while(1):

    # Take each frame
    ret, frame = cap.read()

    frame = segment(frame)
    cv2.imshow('result',frame)

    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()