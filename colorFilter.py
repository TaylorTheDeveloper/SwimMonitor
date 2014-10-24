#!/usr/bin/env python
import numpy as np
import cv2
import cv2.cv as cv


#Create Track bar for hsl values
cv2.namedWindow('control', 0)

h_l = 0
h_u = 179

s_l = 95
s_u = 255

v_l = 0
v_u = 255

def set_scale_h_u(val):
    global h_u
    h_u = val
def set_scale_h_l(val):
    global h_l
    h_l = val
def set_scale_s_u(val):
    global s_u
    s_u = val
def set_scale_s_l(val):
    global s_l
    s_l = val
def set_scale_v_u(val):
    global v_u
    v_u = val
def set_scale_v_l(val):
    global v_l
    v_l = val

cv2.createTrackbar('H_l', 'control', 0, 179, set_scale_h_l)
cv2.createTrackbar('H_u', 'control', 105, 179, set_scale_h_u)

cv2.createTrackbar('S_l', 'control', 95, 255, set_scale_s_l)
cv2.createTrackbar('S_u', 'control', 255, 255, set_scale_s_u)

cv2.createTrackbar('V_l', 'control', 0, 255, set_scale_v_l)
cv2.createTrackbar('V_u', 'control', 255, 255, set_scale_v_u)

help_message = '''
USAGE: colorFilter.py | Hard Code Source Video
'''

if __name__ == '__main__':
    import sys, getopt
    print help_message

    cam = cv2.VideoCapture('MVI_7026_1.avi')

    #Open Cam and load our source details
    ret, img = cam.read()
    src_Height, src_Width, src_Depth = img.shape
    src_Area = src_Width * src_Height

    #Blur
    kernel = np.ones((3,3),np.uint8)

    while True:
        ret, img = cam.read()
        #img = cv2.flip(img,1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([h_l,s_l,v_l]) 
        upper = np.array([h_u,s_u,v_u])

         # Threshold the HSV image to get only blue colors
        imgMask = cv2.inRange(img, lower, upper)
        
        #morphological opening (removes small objects from the foreground)
        #Erode and Expand the edges of the mask to eliminate small artifacts
        imgMask = cv2.erode(imgMask, kernel, iterations=1)
        imgMask = cv2.dilate(imgMask, kernel, iterations=1)

        #morphological opening (removes small objects from the foreground)
        #Erode and Expand the edges of the mask to eliminate small artifacts
        imgMask = cv2.dilate(imgMask, kernel, iterations=1)
        imgMask = cv2.erode(imgMask, kernel, iterations=1)

        cv2.imshow('img',img)
        cv2.imshow('imgMask',imgMask)



        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()