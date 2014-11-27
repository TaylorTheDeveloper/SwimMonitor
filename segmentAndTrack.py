# filterBlue.py
# Taylor Brockhoeft
#
# Ported From Origional C++ code colorFilter.cpp which does the same thing, only in C++
# The Process is somewhat different, I make use of numpy arrays
#
# This Program Outlines how it's possible to use the deep
# blue colors of the pool, agregate them, and then create
# a mask which allows us to segment the swimmers from the water.
#
# It requires a certain degree of calibration, depending on the hues of blue.
# Implementing a trackbar is trivially easy, so for now, this program will be hardcoded. 
# In colorfilter.cpp, you can see how the trackbars affect the mask. In colorFilter.py, 
# the first attempt to re-write this program, you can see good examples on how to implement
# a trackbar.
# 
#

import cv2
import numpy as np

#This Function Segements Swimmers from an image, returns the same image after the mask
def segment(frame):
    """This Function Segments Swimmers from the image, and returns the same frame after the mask"""
    #Blur
    kernel = np.ones((5,5),np.uint8)
    finekernel = np.ones((3,3),np.uint8)
    # define range of blue color in HSV
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([130,255,255])

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    imgMask = cv2.inRange(hsv, lower_blue, upper_blue)

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


while(1):

    # Take each frame
    _, frame = cap.read()

    res = segment(frame)

    cv2.imshow('res',res)

    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()