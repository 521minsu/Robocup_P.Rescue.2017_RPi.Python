######################################
#  Robocup_Junior_2017_Premier_Test  #
# ---------------------------------- # 
#  Description: This program is for  #
#  test usage ONLY. Does not have    #
#  anything that is important.       #
# ---------------------------------- #
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 27.08.17             #
######################################

#Camera & Opencv related modules
from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np

bx,by,gx,gy,rx,ry = 0,0,0,0,0,0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = False


rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(1)

def nothing(x):
    pass


cv2.namedWindow('Black Cal')
cv2.createTrackbar('G','Black Cal',0,255,nothing)
cv2.createTrackbar('Threshold','Black Cal',0,255,nothing)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    Mimage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    G = cv2.getTrackbarPos('G','Black Cal')
    T = cv2.getTrackbarPos('Threshold','Black Cal')
    
    Blower = np.array([0,0,0],dtype="uint8")
    Bupper = np.array([255,G,255],dtype="uint8")
    Bmask = cv2.inRange(image,Blower,Bupper)
    
    thresh,inv_black = cv2.threshold(Bmask,127,255,cv2.THRESH_BINARY_INV)
    
    thresh,blackplusgreen = cv2.threshold(Mimage,T,255,cv2.THRESH_BINARY_INV)
    
    test1 = cv2.bitwise_and(image,image,mask=inv_black)
    test2 = cv2.bitwise_and(test1,test1,mask=blackplusgreen)
    
    testA = cv2.bitwise_and(image,image,mask=Bmask)
    
    blackview = testA[150:210, 0:320]
    greenview = test2[30:90, 0:320]  #150,210
    
    cv2.imshow("Black View", blackview)
    cv2.imshow("Green View",greenview)
    cv2.imshow("test1",test1)
    cv2.imshow("test2",test2)
    cv2.imshow("image",image)
    
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
      

