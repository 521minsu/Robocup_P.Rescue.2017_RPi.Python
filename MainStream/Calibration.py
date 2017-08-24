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
camera.hflip = False

rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)

def nothing(x):
    pass

# create Window called 'setting' to call in order to add trackbars
cv2.namedWindow('Black Cal')
cv2.namedWindow('Green Cal')
cv2.namedWindow('Orange Cal')
cv2.namedWindow('customDotSetup')
cv2.namedWindow('Camera Angle')

# adding trackbars to the window called 'setting'
cv2.createTrackbar('Min R','Black Cal',0,255,nothing)
cv2.createTrackbar('Min G','Black Cal',0,255,nothing)
cv2.createTrackbar('Min B','Black Cal',0,255,nothing)
cv2.createTrackbar('Max R','Black Cal',0,255,nothing)
cv2.createTrackbar('Max G','Black Cal',0,255,nothing)
cv2.createTrackbar('Max B','Black Cal',0,255,nothing)

cv2.createTrackbar('Min H','Green Cal',0,255,nothing)
cv2.createTrackbar('Min S','Green Cal',0,255,nothing)
cv2.createTrackbar('Min V','Green Cal',0,255,nothing)
cv2.createTrackbar('Max H','Green Cal',0,255,nothing)
cv2.createTrackbar('Max S','Green Cal',0,255,nothing)
cv2.createTrackbar('Max V','Green Cal',0,255,nothing)

cv2.createTrackbar('Min H','Orange Cal',0,255,nothing)
cv2.createTrackbar('Min S','Orange Cal',0,255,nothing)
cv2.createTrackbar('Min V','Orange Cal',0,255,nothing)
cv2.createTrackbar('Max H','Orange Cal',0,255,nothing)
cv2.createTrackbar('Max S','Orange Cal',0,255,nothing)
cv2.createTrackbar('Max V','Orange Cal',0,255,nothing)
cv2.createTrackbar('Min Area','Orange Cal',0,255,nothing)

cv2.createTrackbar('X: Custom Dot','customDotSetup',0,320,nothing)
cv2.createTrackbar('Y: Custom Dot','customDotSetup',0,240,nothing)

cv2.createTrackbar('On : Off','Camera Angle',0,1,nothing)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # image feeds to apply masks on
        image = frame.array
        Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        Oimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        # blurred image to show detection status
        blur = cv2.blur(image, (3,3))
        Bblur = cv2.blur(image, (3,3))
        Gblur = cv2.blur(image, (3,3))
        Oblur = cv2.blur(image, (3,3))
        Dblur = cv2.blur(image, (3,3))
        Eblur = cv2.blur(image, (3,3))
        
        Min_BR = cv2.getTrackbarPos('Min R','Black Cal')
        Min_BG = cv2.getTrackbarPos('Min G','Black Cal')
        Min_BB = cv2.getTrackbarPos('Min B','Black Cal')
        Max_BR = cv2.getTrackbarPos('Max R','Black Cal')
        Max_BG = cv2.getTrackbarPos('Max G','Black Cal')
        Max_BB = cv2.getTrackbarPos('Max B','Black Cal')
        
        Min_GH = cv2.getTrackbarPos('Min H','Green Cal')
        Min_GS = cv2.getTrackbarPos('Min S','Green Cal')
        Min_GV = cv2.getTrackbarPos('Min V','Green Cal')
        Max_GH = cv2.getTrackbarPos('Max H','Green Cal')
        Max_GS = cv2.getTrackbarPos('Max S','Green Cal')
        Max_GV = cv2.getTrackbarPos('Max V','Green Cal')
        
        Min_OH = cv2.getTrackbarPos('Min H','Orange Cal')
        Min_OS = cv2.getTrackbarPos('Min S','Orange Cal')
        Min_OV = cv2.getTrackbarPos('Min V','Orange Cal')
        Max_OH = cv2.getTrackbarPos('Max H','Orange Cal')
        Max_OS = cv2.getTrackbarPos('Max S','Orange Cal')
        Max_OV = cv2.getTrackbarPos('Max V','Orange Cal')
        Min_OA = cv2.getTrackbarPos('Min Area','Orange Cal')
        
        CDX = cv2.getTrackbarPos('X: Custom Dot','customDotSetup')
        CDY = cv2.getTrackbarPos('Y: Custom Dot','customDotSetup')
        
        CVal = cv2.getTrackbarPos('On : Off','Camera Angle')
        
        #For Black, start with Min(0,0,0) Max(255,0,255), when calibrating
        Blower = np.array([Min_BR,Min_BG,Min_BB],dtype="uint8")
        Bupper = np.array([Max_BR,Max_BG,Max_BB],dtype="uint8")
        #For Green, start with Min(50,0,60) Max(89,255,255), when calibrating
        Glower = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8")
        Gupper = np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
        #For Orange, start with Min(146,149,88) Max(220,222,255), when calibrating
        Olower = np.array([Min_OH,Min_OS,Min_OV],dtype="uint8")
        Oupper = np.array([Max_OH,Max_OS,Max_OV],dtype="uint8")
        #If CVal is 1, lift the camera
        if CVal == 1:
            cc(cc,'up')
        elif CVal == 0:
            cc(cc,'down')
        
        # Apply mask that is created by detecting colors
        Bmask = cv2.inRange(image,Blower,Bupper)
        Gmask = cv2.inRange(Gimage,Glower,Gupper)
        Omask = cv2.inRange(Oimage,Olower,Oupper)
        
        # Apply vision limiters (Forced Mask over mask that is created by detecting color)
        visionmask=cv2.imread('mask_noside.png',0)
        resvisionmask=cv2.imread('rescue_mask.png',0)
        res = cv2.bitwise_and(Bmask,Bmask,mask=visionmask)
        Gres = cv2.bitwise_and(Gmask,Gmask,mask=visionmask)
        Ores = cv2.bitwise_and(Omask,Omask,mask=resvisionmask)
        
        # find contours in the threshold image
        res, Rcontours,Rhierarchy = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gres, GRcontours,GRhierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Ores, ORcontours,ORhierarchy = cv2.findContours(Ores,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
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
        
        
        # finding contour with maximum area and store it as best_cnt - Green Patch (Mask Applied)
        min_area = 1000
        best_cnt = 1
        for cnt in GRcontours:
                area = cv2.contourArea(cnt)
                if area > min_area:
                        min_area = area
                        best_cnt = cnt
        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        gx,gy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        # gx, gy = green area following yellow dot
        
        
        # finding contour with maximum area and store it as best_cnt - Rescue Area
        min_area = Min_OA
        best_cnt = 1
        for cnt in ORcontours:
                area = cv2.contourArea(cnt)
                if area > min_area:
                        min_area = area
                        best_cnt = cnt
        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        ox,oy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        # rx, ry = Pink dot when Rescue has been reached.
        
        
        # Mapping dots on image based on Black mask
        if cx != 0 or cy != 0:
            cv2.circle(Eblur,(cx,cy),5,(0,0,255),-1)
            cv2.circle(Bblur,(cx,cy),5,(0,0,255),-1)
        # Mapping dots on image based on Green mask
        if gx != 0 or gy != 0:
            cv2.circle(Eblur,(gx,gy),5,(0,255,255),-1)
            cv2.circle(Gblur,(gx,gy),5,(0,255,255),-1)
        # Mapping dots on image based on Orange mask
        if ox != 0 or oy != 0:
            cv2.circle(Eblur,(ox,oy),5,(255,0,255),-1)
            cv2.circle(Oblur,(ox,oy),5,(255,0,255),-1)
        # Mapping dots on image based on the input from trackbars
        if CDX != 0 or CDY != 0:
            cv2.circle(Eblur,(CDX,CDY),5,(255,255,255),-1) 
            cv2.circle(Dblur,(CDX,CDY),5,(255,255,255),-1)
        # Mapping center dot on image
        cv2.circle(Eblur,(170,160),5,(0,255,0),-1)
        
        # images with trackbars
        cv2.imshow("Black Cal",Bmask)      # Shows black mask without vision limiter with Black Cal Trackbars
        cv2.imshow("Green Cal",Gmask)     # Shows green mask without vision limiter with Green Cal Trackbars
        cv2.imshow("Orange Cal",Omask)    # Shows orange mask without vision limiter with Orange Cal Trackbars
        cv2.imshow("customDotSetup",Dblur) # Shows image with a dot that can be moved by CDS Trackbars with CDS Trackbars
        
        # images without trackbars
##        cv2.imshow("Pure Stream",blur)      # Shows the pure image input to RPi/opencv
##        cv2.imshow("Masked Black",res)      # Shows black mask with vision limiter
##        cv2.imshow("Black Dot View",Bblur)  # Shows a dot where the black color is detected on a pure image
##        cv2.imshow("Masked Green",Gres)     # Shows green mask with vision limiter
##        cv2.imshow("Green Dot View",Gblur)  # Shows a dot where the green color is detected on a pure image
        cv2.imshow("Masked Orange",Ores)    # Shows orange mask with vision limiter
        cv2.imshow("Orange Dot View",Oblur) # Shows a dot where the orange color is detected on a pure image
        cv2.imshow("All Dots View",Eblur)   # Shows every dots that has been mapped during this time.

        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            break

        
