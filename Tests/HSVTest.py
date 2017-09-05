######################################
#  Robocup_Junior_2017_Premier_Main  #
# ---------------------------------- # 
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 24.07.17             #
######################################

from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np
##import dc_motors.py
##import servo_motors.py
##
##motors = dc_motors.py
##servos = servo_motors.py

MIN_MATCH_COUNT=6

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)

def nothing(x):
    pass

cv2.namedWindow('setting')

cv2.createTrackbar('Min BH','setting',0,255,nothing)
cv2.createTrackbar('Min BS','setting',0,255,nothing)
cv2.createTrackbar('Min BV','setting',0,255,nothing)
cv2.createTrackbar('Max BH','setting',0,255,nothing)
cv2.createTrackbar('Max BS','setting',0,255,nothing)
cv2.createTrackbar('Max BV','setting',0,255,nothing)

cv2.createTrackbar('Min GH','setting',0,255,nothing)
cv2.createTrackbar('Min GS','setting',0,255,nothing)
cv2.createTrackbar('Min GV','setting',0,255,nothing)
cv2.createTrackbar('Max GH','setting',0,255,nothing)
cv2.createTrackbar('Max GS','setting',0,255,nothing)
cv2.createTrackbar('Max GV','setting',0,255,nothing)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        Gimage = copy(image)

        blur = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        Gblur = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

        Min_BB = cv2.getTrackbarPos('Min BH','setting')
        Min_BG = cv2.getTrackbarPos('Min BS','setting')
        Min_BR = cv2.getTrackbarPos('Min BV','setting')
        Max_BB = cv2.getTrackbarPos('Max BH','setting')
        Max_BG = cv2.getTrackbarPos('Max BS','setting')
        Max_BR = cv2.getTrackbarPos('Max BV','setting')
        
        Min_GB = cv2.getTrackbarPos('Min GH','setting')
        Min_GG = cv2.getTrackbarPos('Min GS','setting')
        Min_GR = cv2.getTrackbarPos('Min GV','setting')
        Max_GB = cv2.getTrackbarPos('Max GH','setting')
        Max_GG = cv2.getTrackbarPos('Max GS','setting')
        Max_GR = cv2.getTrackbarPos('Max GV','setting')
        #print("For Black, Min B:{} G:{} R:{} Max B:{} G:{} R:{} For Green, Min B:{} G:{} R:{} Max B:{} G:{} R:{}".format(Min_BB,Min_BG,Min_BR,Max_BB,Max_BG,Max_BR,Min_GB,Min_GG,Min_GR,Max_GB,Max_GG,Max_GR))
        
        #For Black, start with Min(0,0,0) Max(16,255,255), when calibrating
        Blower = np.array([Min_BB,Min_BG,Min_BR],dtype="uint8")
        Bupper = np.array([Max_BB,Max_BG,Max_BR],dtype="uint8")
        #For Green, start with Min(0,33,0) Max(220,255,51), when calibrating
        Glower = np.array([Min_GB,Min_GG,Min_GR],dtype="uint8")
        Gupper = np.array([Max_GB,Max_GG,Max_GR],dtype="uint8")

        Gmask = cv2.inRange(Gblur,Glower,Gupper)
        Bmask = cv2.inRange(blur,Blower,Bupper)
        
        res = cv2.bitwise_and(blur,blur,mask=Bmask)
        Gres = cv2.bitwise_and(Gblur,Gblur,mask=Gmask)

        cv2.imshow("setting",image) 
        cv2.imshow("GreenMask",Gimage)
        cv2.imshow("MaskedBlack",res)
        cv2.imshow("MaskedGreen",Gres)

        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            break

