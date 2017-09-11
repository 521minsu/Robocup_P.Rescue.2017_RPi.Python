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
#  Last Update: 22.08.17              #
#######################################

from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np
import dc_motors
cc = dc_motors.Motor.cameracontrol

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

# create Window called 'setting' to call in order to add trackbars
cv2.namedWindow('Black Cal')
cv2.namedWindow('Green Cal')
cv2.namedWindow('Camera')

# adding trackbars to the window called 'setting'
cv2.createTrackbar('Min B','Black Cal',0,255,nothing)
cv2.createTrackbar('Min G','Black Cal',0,255,nothing)
cv2.createTrackbar('Min R','Black Cal',0,255,nothing)
cv2.createTrackbar('Max B','Black Cal',0,255,nothing)
cv2.createTrackbar('Max G','Black Cal',0,255,nothing)
cv2.createTrackbar('Max R','Black Cal',0,255,nothing)

cv2.createTrackbar('Min H','Green Cal',0,255,nothing)
cv2.createTrackbar('Min S','Green Cal',0,255,nothing)
cv2.createTrackbar('Min V','Green Cal',0,255,nothing)
cv2.createTrackbar('Max H','Green Cal',0,255,nothing)
cv2.createTrackbar('Max S','Green Cal',0,255,nothing)
cv2.createTrackbar('Max V','Green Cal',0,255,nothing)
cv2.createTrackbar('Min Area','Green Cal',0,80000,nothing)

cv2.createTrackbar('Camera Lift', 'Camera',0,1,nothing)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # image feeds to apply masks on
        original = frame.array
        image = cv2.flip(original,0)
        Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        # blurred image to show detection status
        blur = cv2.blur(image, (3,3))
        Bblur = cv2.blur(image, (3,3))
        Gblur = cv2.blur(image, (3,3))
        Eblur = cv2.blur(image, (3,3))
        
        Min_BB = cv2.getTrackbarPos('Min B','Black Cal')
        Min_BG = cv2.getTrackbarPos('Min G','Black Cal')
        Min_BR = cv2.getTrackbarPos('Min R','Black Cal')
        Max_BB = cv2.getTrackbarPos('Max B','Black Cal')
        Max_BG = cv2.getTrackbarPos('Max G','Black Cal')
        Max_BR = cv2.getTrackbarPos('Max R','Black Cal')
        
        Min_GH = cv2.getTrackbarPos('Min H','Green Cal')
        Min_GS = cv2.getTrackbarPos('Min S','Green Cal')
        Min_GV = cv2.getTrackbarPos('Min V','Green Cal')
        Max_GH = cv2.getTrackbarPos('Max H','Green Cal')
        Max_GS = cv2.getTrackbarPos('Max S','Green Cal')
        Max_GV = cv2.getTrackbarPos('Max V','Green Cal')
        Min_GA = cv2.getTrackbarPos('Min Area','Green Cal')
        
        camera = cv2.getTrackbarPos('Camera Lift','Camera')
        
        if camera == 0:
            cc(cc,'down')
        elif camera == 1:
            cc(cc,'up')
        
        #For Black, start with 50, when calibrating
        Blower = np.array([Min_BB,Min_BG,Min_BR],dtype="uint8")
        Bupper = np.array([Max_BB,Max_BG,Max_BR],dtype="uint8")
        #For Green, start with Min(20,60,50) Max(80,200,200), when calibrating
        Glower = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8")
        Gupper = np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
##        Glower = np.array([120,10,70],dtype="uint8")
##        Gupper = np.array([180,175,155],dtype="uint8")
        
        # Apply mask that is created by detecting colors
        Bmask = cv2.inRange(image,Blower,Bupper)
        Gmask = cv2.inRange(Gimage,Glower,Gupper)
        
        # Apply vision limiters (Forced Mask over mask that is created by detecting color)
        res = Bmask[30:90]
        Bres = Bmask[150:210]
        Gres = Gmask[150:210]
        
        # find contours in the threshold image
        res, Rcontours,Rhierarchy = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gres, GRcontours,GRhierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Bres, BRcontours,BRhierarchy = cv2.findContours(Bres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        # finding contour with maximum area and store it as best_cnt - Black Line (Mask Applied)
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
        
        # finding contour with maximum area and store it as best_cnt - Black Line (Mask Applied)
        min_area = 0
        best_cnt = 1
        for cnt in BRcontours:
                area = cv2.contourArea(cnt)
                if area > min_area:
                        min_area = area
                        best_cnt = cnt
        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        # cx, cy = black line following red dot
        bx,by = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        
        # finding contour with maximum area and store it as best_cnt - Green Patch (Mask Applied)
        min_area = Min_GA
        best_cnt = 1
        for cnt in GRcontours:
                area = cv2.contourArea(cnt)
                if area > min_area:
                        min_area = area
                        best_cnt = cnt
        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        gx,gy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        
        # Mapping dots on image based on Black mask
        if cx != 0 or cy != 0:
            cv2.circle(Eblur,(cx,cy),5,(0,0,255),-1)
            cv2.circle(Bblur,(cx,cy),5,(0,0,255),-1)
        if bx != 0 or by != 0:
            cv2.circle(Eblur,(bx,by),5,(0,0,255),-1)
            cv2.circle(Bblur,(bx,by),5,(0,0,255),-1)
        # Mapping dots on image based on Green mask
        if gx != 0 or gy != 0:
            cv2.circle(Eblur,(gx,gy),5,(0,255,255),-1)
            cv2.circle(Gblur,(gx,gy),5,(0,255,255),-1)
        # Mapping center dot on image
        cv2.circle(Eblur,(170,160),5,(0,255,0),-1)
        
        # images with trackbars
        cv2.imshow("Black Cal",Bmask)      # Shows black mask without vision limiter with Black Cal Trackbars
        cv2.imshow("Green Cal",Gmask)     # Shows green mask without vision limiter with Green Cal Trackbars
        # images without trackbars
        cv2.imshow("All Dots View",Eblur)   # Shows every dots that has been mapped during this time.

        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            break

        
