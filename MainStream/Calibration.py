#######################################
#  Robocup_Junior_2017_Premier_Calib  #
# ----------------------------------  # 
#  Description: This program allows   #
#  user to change detection range     #
#  with Trackbars. Used to send color #
#  ranges to Main.py in the same dir  #
# ----------------------------------- #
#  Author: Minsu Kim                  #
#  Email : 521minsu@gmail.com         #
#  Last Update: 28.07.17              #
#######################################

from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = False

rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)

def nothing(x):
    pass

# create Window called 'setting' to call in order to add trackbars
cv2.namedWindow('setting')
cv2.namedWindow('customDotSetup')

# adding trackbars to the window called 'setting'
cv2.createTrackbar('Min BR','setting',0,255,nothing)
cv2.createTrackbar('Min BG','setting',0,255,nothing)
cv2.createTrackbar('Min BB','setting',0,255,nothing)
cv2.createTrackbar('Max BR','setting',0,255,nothing)
cv2.createTrackbar('Max BG','setting',0,255,nothing)
cv2.createTrackbar('Max BB','setting',0,255,nothing)

cv2.createTrackbar('Min GH','setting',0,255,nothing)
cv2.createTrackbar('Min GS','setting',0,255,nothing)
cv2.createTrackbar('Min GV','setting',0,255,nothing)
cv2.createTrackbar('Max GH','setting',0,255,nothing)
cv2.createTrackbar('Max GS','setting',0,255,nothing)
cv2.createTrackbar('Max GV','setting',0,255,nothing)

cv2.createTrackbar('X: Custom Dot','customDotSetup',0,320,nothing)
cv2.createTrackbar('Y: Custom Dot','customDotSetup',0,240,nothing)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        blur = cv2.blur(image, (3,3))
        
        Min_BR = cv2.getTrackbarPos('Min BR','setting')
        Min_BG = cv2.getTrackbarPos('Min BG','setting')
        Min_BB = cv2.getTrackbarPos('Min BB','setting')
        Max_BR = cv2.getTrackbarPos('Max BR','setting')
        Max_BG = cv2.getTrackbarPos('Max BG','setting')
        Max_BB = cv2.getTrackbarPos('Max BB','setting')
        
        Min_GH = cv2.getTrackbarPos('Min GH','setting')
        Min_GS = cv2.getTrackbarPos('Min GS','setting')
        Min_GV = cv2.getTrackbarPos('Min GV','setting')
        Max_GH = cv2.getTrackbarPos('Max GH','setting')
        Max_GS = cv2.getTrackbarPos('Max GS','setting')
        Max_GV = cv2.getTrackbarPos('Max GV','setting')
        
        CDX = cv2.getTrackbarPos('X: Custom Dot','customDotSetup')
        CDY = cv2.getTrackbarPos('Y: Custom Dot','customDotSetup')
        
        #For Black, start with Min(0,0,0) Max(255,0,255), when calibrating
        Blower = np.array([Min_BR,Min_BG,Min_BB],dtype="uint8")
        Bupper = np.array([Max_BR,Max_BG,Max_BB],dtype="uint8")
        #For Green, start with Min(50,0,60) Max(89,255,255), when calibrating
        Glower = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8")
        Gupper = np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
        
        Gmask = cv2.inRange(Gimage,Glower,Gupper)
        Bmask = cv2.inRange(image,Blower,Bupper)
        
        # find contours in the threshold image
        image, contours,hierarchy = cv2.findContours(Bmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gimage, Gcontours,Ghierarchy = cv2.findContours(Gmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        visionmask=cv2.imread('mask320.png',0)
        res = cv2.bitwise_and(Bmask,Bmask,mask=visionmask)
        Gres = cv2.bitwise_and(Gmask,Gmask,mask=visionmask)
        
        res, Rcontours,Rhierarchy = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gres, GRcontours,GRhierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
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
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
        
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
        gx,gy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        # gx, gy = green area following yellow dot
        cv2.circle(blur,(gx,gy),10,(0,255,255),-1)
        
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
        rx,ry = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        # rx, ry = Pink dot when Rescue has been reached.
        cv2.circle(blur,(rx,ry),10,(255,0,255),-1)
        
        # green dot where the middle line of the video feed is
        cv2.circle(blur,(170,160),10,(0,255,0),-1)
        cv2.circle(blur,(CDX,CDY),5,(255,255,255),-1)
        print("x:{} y:{}".format(cx,cy))
        
        # show the frame
        cv2.imshow("setting",image)
        cv2.imshow("customDotSetup",blur)
        cv2.imshow("Frame", blur)
        cv2.imshow("GreenMask",Gimage)
        cv2.imshow("BlackMask",image)
        cv2.imshow("MaskedBlack",res)
        cv2.imshow("MaskedGreen",Gres)

        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            break

        
