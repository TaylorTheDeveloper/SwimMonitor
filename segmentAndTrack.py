# filterBlue.py
# Taylor Brockhoeft
#
# This program attempts to segment, and then track, swimmers in a pool.
# Current Status: not working
#
# May need to go about it a different way. This method attempts to get the differences to determine motion
# 
#

import cv2
import numpy as np

#Global Constants
MHI_DURATION = 0.5
DEFAULT_THRESHOLD = 32
MAX_TIME_DELTA = 0.25
MIN_TIME_DELTA = 0.05

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
cv2.namedWindow('swimtracker')
cv2.createTrackbar('threshold', 'swimtracker', DEFAULT_THRESHOLD, 255, nothing)

ret, frame = cap.read()
#h, w = frame.shape[:2]
prev_frame = frame.copy()
prev_frame = segment(prev_frame)
h, w = frame.shape[:2]
motion_history = np.zeros((h, w), np.float32)
hsv = np.zeros((h, w, 3), np.uint8)
hsv[:,:,1] = 255

while(1):

    # Take each frame
    ret, frame = cap.read()

    frame = segment(frame)


    frame_diff = cv2.absdiff(frame, prev_frame)
    gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)#
    thrs = cv2.getTrackbarPos('threshold', 'swimtracker')
    ret, motion_mask = cv2.threshold(gray_diff, thrs, 1, cv2.THRESH_BINARY)
    timestamp = cv2.getTickCount() / cv2.getTickFrequency()
    cv2.updateMotionHistory(motion_mask, motion_history, timestamp, MHI_DURATION)
    mg_mask, mg_orient = cv2.calcMotionGradient( motion_history, MAX_TIME_DELTA, MIN_TIME_DELTA, apertureSize=5 )
    seg_mask, seg_bounds = cv2.segmentMotion(motion_history, timestamp, MAX_TIME_DELTA)

    for i, rect in enumerate([(0, 0, w, h)] + list(seg_bounds)):
        x, y, rw, rh = rect
        area = rw*rh
        if area < 64**2:
            continue
        silh_roi   = motion_mask   [y:y+rh,x:x+rw]
        orient_roi = mg_orient     [y:y+rh,x:x+rw]
        mask_roi   = mg_mask       [y:y+rh,x:x+rw]
        mhi_roi    = motion_history[y:y+rh,x:x+rw]
        if cv2.norm(silh_roi, cv2.NORM_L1) < area*0.05:
            continue
        angle = cv2.calcGlobalOrientation(orient_roi, mask_roi, mhi_roi, timestamp, MHI_DURATION)
        color = ((255, 0, 0), (0, 0, 255))[i == 0]
        draw_motion_comp(frame, rect, angle, color)

    cv2.imshow('result',frame)

    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()