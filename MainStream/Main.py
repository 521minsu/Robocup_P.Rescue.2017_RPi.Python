######################################
#  Robocup_Junior_2017_Premier_Main  #
# ---------------------------------- # 
#  Description: This program detects #
#  colors and sends the results to   #
#  Loop.py in the same directory     #
# ---------------------------------- #
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 08.08.17             #
######################################

##############################################
# !!!!!!! DO NOT FORGET TO CALIBRATE !!!!!!! #
##############################################

#Camera & Opencv related modules
from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np

#Loop and program related modules
from Loop import MainControl as Mainloop
import SensorReading as SR
import rescue
Rescue = False
CatchIt = False
finished = False

import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
cc = dc_motors.Motor.cameracontrol

# Check these before running
#######################################
motor_ENABLE = True                   #
#######################################
green_ENABLE = True                   #
#######################################
waterTower_ENABLE = False             #
WTLimit = 0                           #
#######################################
WTDone = 0

bx,by,gx,gy,rx,ry = 0,0,0,0,0,0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = False

cc(cc,'down')

rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):      
    #Make sure You are putting calibrated values in
    Min_BB,Min_BG,Min_BR = 0,0,0
    Max_BB,Max_BG,Max_BR = 255,47,255
    
    Min_GH,Min_GS,Min_GV = 21,63,54
    Max_GH,Max_GS,Max_GV = 80,196,197
    
    # image from the Picam
    original = frame.array
    hflip = cv2.flip(original,0)
    image = cv2.flip(hflip,1)
    # images from the Picam with filters and effects
    Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    blur = cv2.blur(image, (3,3))
    
    #Please Run Calibration.py first, and bring back the values according to the current situation
    Blower = np.array([Min_BB,Min_BG,Min_BR],dtype="uint8")
    Bupper = np.array([Max_BB,Max_BG,Max_BR],dtype="uint8")
    #Please Run Calibration.py first, and bring back the values according to the current situation
    Glower = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8")
    Gupper = np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
    
    # Pure Masked image without any limits on its vision
    Gmask = cv2.inRange(Gimage,Glower,Gupper)
    Bmask = cv2.inRange(image,Blower,Bupper)
    
    #########################################
    #   Finding contours for line tracing   #
    #########################################
    Bres = Bmask[30:90]
    Gres = Gmask[150:210]
    
    Bres, Rcontours,Rhierarchy = cv2.findContours(Bres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Gres, Gcontours,Ghierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
    # finding contour with maximum area and store it as best_cnt - Black Area
    min_area = 0
    best_cnt = 1
    for cnt in Rcontours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                    min_area = area
                    best_cnt = cnt
    
    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    # cx, cy = black line following red dot
    bx,by = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    
    # finding contour with maximum area and store it as best_cnt - Green Area
    min_area = 1000 # Was 530 before
    best_cnt = 1
    for cnt in Gcontours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                    min_area = area
                    best_cnt = cnt
    
    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    # gx, gy = green area following yellow dot
    gx,gy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    
    
    # green dot where the middle line of the video feed is
    cv2.circle(blur,(gx,gy),5,(255,0,0),-1)      # Blue Dot
    cv2.circle(blur,(bx,by),5,(0,0,255),-1)      # Red Dot
    cv2.circle(blur,(170,160),5,(0,255,0),-1)    # Green Dot
    lineerror,turnerror = 1000,1000
    
    # Gets the distance Value, but reads 5 times so there's no typeError when going through rest of the program
    for i in range(0,5):
        dist = SR.value('distance')
    
    
    if bx != 0 and motor_ENABLE == True:
        lineerror = bx - 170
        Mainloop.linetrace(Mainloop,lineerror)
        print("From Main.py Black... obstacle:{}cm".format(dist))
    if gx != 0 and bx != 0 and motor_ENABLE == True and green_ENABLE == True:
        turnerror = gx - bx
        Mainloop.greenturn(Mainloop,turnerror)
    if waterTower_ENABLE == True and WTDone < WTLimit:
        Mainloop.watertower(Mainloop,dist)
        WTDone += 1
        print("From Main.py WT... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t obstacle:{}cm".format(lineerror,bx,by,gx,gy,dist))
    else:
        print("From Main.py else... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t distance:{}cm".format(lineerror,bx,by,gx,gy,dist))
    
    cv2.imshow("result",blur)
    #cv2.imshow("Gmask",Gmask)
    #cv2.imshow("Gres",Gres)
    #cv2.imshow("Bmask",Bmask)
    #cv2.imshow("Bres",res)
    
    key = cv2.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    print(dist)

