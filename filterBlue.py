import cv2
import numpy as np

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('MVI_7026.mp4')

#Blur
kernel = np.ones((3,3),np.uint8)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    imgMask = cv2.inRange(hsv, lower_blue, upper_blue)

    
    #morphological opening (removes small objects from the foreground)
    #Erode and Expand the edges of the mask to eliminate small artifacts
    imgMask = cv2.erode(imgMask, kernel, iterations=1)
    imgMask = cv2.dilate(imgMask, kernel, iterations=1)

    #morphological opening (removes small objects from the foreground)
    #Erode and Expand the edges of the mask to eliminate small artifacts
    imgMask = cv2.dilate(imgMask, kernel, iterations=1)
    imgMask = cv2.erode(imgMask, kernel, iterations=1)
    
    #InvertMask
    imgMask = cv2.bitwise_not(imgMask,imgMask)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= imgMask)

    cv2.imshow('res',res)

    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()