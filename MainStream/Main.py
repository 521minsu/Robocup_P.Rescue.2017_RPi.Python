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

#Camera & Opencv related modules
from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np

#Loop and program related modules
import Loop
Mainloop = Loop.MainControl
import ultraSonicReading as USR

# Check these before running
#######################################
motor_ENABLE = False                  #
#######################################
green_ENABLE = False                  #
#######################################
waterTower_ENABLE = False             #
WTLimit = 1                           #
#######################################

WTDone = 0

bx,by,gx,gy,rx,ry = 0,0,0,0,0,0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = False

rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)

# Read images from the directory
visionmask = cv2.imread('/images/mask320.png',0)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # image from the Picam
    image = frame.array
    # images from the Picam with filters and effects
    Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    blur = cv2.blur(image, (3,3))
    
    Min_BB,Min_BG,Min_BR = 0,0,0
    Max_BB,Max_BG,Max_BR = 255,50,255
    
    Min_GH,Min_GS,Min_GV = 24,0,38
    Max_GH,Max_GS,Max_GV = 85,255,255
    
    #Please Run Calibration.py first, and bring back the values according to the current situation
    Blower = np.array([Min_BB,Min_BG,Min_BR],dtype="uint8")
    Bupper = np.array([Max_BB,Max_BG,Max_BR],dtype="uint8")
    #Please Run Calibration.py first, and bring back the values according to the current situation
    Glower = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8")
    Gupper = np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
    
    Gmask = cv2.inRange(Gimage,Glower,Gupper)
    Bmask = cv2.inRange(image,Blower,Bupper)
    
    res = cv2.bitwise_and(Bmask,Bmask,mask=visionmask)
    Gmask = cv2.bitwise_and(Gmask,Gmask,mask=visionmask)
    
    # find contours in the threshold image
    image, contours,hierarchy = cv2.findContours(Bmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Gimage, Gcontours,Ghierarchy = cv2.findContours(Gmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    res, Rcontours,Rhierarchy = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Gres, GRcontours,GRhierarchy = cv2.findContours(Gmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
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
    min_area = 1000
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
    
    # finding contour with maximum area and store it as best_cnt - Rescue Area
    min_area = 153300
    best_cnt = 1
    for cnt in Gcontours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                    min_area = area
                    best_cnt = cnt
    
    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    # rx, ry = Pink dot when Rescue has been reached.
    rx,ry = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    
    
    # green dot where the middle line of the video feed is
    cv2.circle(blur,(rx,ry),5,(255,255,0),-1)
    cv2.circle(blur,(gx,gy),5,(255,0,0),-1)
    cv2.circle(blur,(bx,by),5,(0,0,255),-1)
    cv2.circle(blur,(170,160),5,(0,255,0),-1)
    lineerror,turnerror = 1000,1000
    
    if bx != 0 and motor_ENABLE == True:
        lineerror = bx - 170
        Mainloop.linetrace(Mainloop,lineerror)
    if gx != 0 and bx != 0 and motor_ENABLE == True and green_ENABLE == True:
        turnerror = gx - bx
        Mainloop.greenturn(Mainloop,turnerror)
    if waterTower_ENABLE == True and WTDone <= WTLimit:
        ultraSonicVal = USR.ultraSonic.value()
        Mainloop.watertower(Mainloop,ultraSonicVal)
        WTDone += 1
        print("From Main.py ... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t obstacle:{}cm".format(lineerror,bx,by,gx,gy,ultraSonicVal))
    else:
        ultrasVal = USR.ultraSonic.value()
        print("From Main.py ... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t distance:{}cm".format(lineerror,bx,by,gx,gy,ultrasVal))
    
    cv2.imshow("result",blur)
    cv2.imshow("Gmask",Gmask)
    cv2.imshow("Gres",Gres)
    
    
    key = cv2.waitKey(1) & 0xFF
    
    	      # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    	      # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        cv2.destroyAllWindows()
        break

