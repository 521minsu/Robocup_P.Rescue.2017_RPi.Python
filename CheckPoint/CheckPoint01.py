# Black Line Detection, Green Area Detection, Rescue Detection COMPLETE


# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np

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

cv2.createTrackbar('Min BB','setting',0,255,nothing)
cv2.createTrackbar('Min BG','setting',0,255,nothing)
cv2.createTrackbar('Min BR','setting',0,255,nothing)
cv2.createTrackbar('Max BB','setting',0,255,nothing)
cv2.createTrackbar('Max BG','setting',0,255,nothing)
cv2.createTrackbar('Max BR','setting',0,255,nothing)

cv2.createTrackbar('Min GB','setting',0,255,nothing)
cv2.createTrackbar('Min GG','setting',0,255,nothing)
cv2.createTrackbar('Min GR','setting',0,255,nothing)
cv2.createTrackbar('Max GB','setting',0,255,nothing)
cv2.createTrackbar('Max GG','setting',0,255,nothing)
cv2.createTrackbar('Max GR','setting',0,255,nothing)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        Gimage = copy(image)

        blur = cv2.blur(image, (3,3))
        Gblur = cv2.blur(Gimage, (1,1))

        Min_BB = cv2.getTrackbarPos('Min BB','setting')
        Min_BG = cv2.getTrackbarPos('Min BG','setting')
        Min_BR = cv2.getTrackbarPos('Min BR','setting')
        Max_BB = cv2.getTrackbarPos('Max BB','setting')
        Max_BG = cv2.getTrackbarPos('Max BG','setting')
        Max_BR = cv2.getTrackbarPos('Max BR','setting')
        
        Min_GB = cv2.getTrackbarPos('Min GB','setting')
        Min_GG = cv2.getTrackbarPos('Min GG','setting')
        Min_GR = cv2.getTrackbarPos('Min GR','setting')
        Max_GB = cv2.getTrackbarPos('Max GB','setting')
        Max_GG = cv2.getTrackbarPos('Max GG','setting')
        Max_GR = cv2.getTrackbarPos('Max GR','setting')
        #print("For Black, Min B:{} G:{} R:{} Max B:{} G:{} R:{} For Green, Min B:{} G:{} R:{} Max B:{} G:{} R:{}".format(Min_BB,Min_BG,Min_BR,Max_BB,Max_BG,Max_BR,Min_GB,Min_GG,Min_GR,Max_GB,Max_GG,Max_GR))
        
        #For Black, start with Min(0,0,0) Max(16,255,255), when calibrating
        Blower = np.array([Min_BB,Min_BG,Min_BR],dtype="uint8")
        Bupper = np.array([Max_BB,Max_BG,Max_BR],dtype="uint8")
        #For Green, start with Min(0,33,0) Max(220,255,51), when calibrating
        Glower = np.array([Min_GB,Min_GG,Min_GR],dtype="uint8")
        Gupper = np.array([Max_GB,Max_GG,Max_GR],dtype="uint8")

        thresh = cv2.inRange(blur,Blower,Bupper)
        Gthresh = cv2.inRange(Gblur,Glower,Gupper)
        Gmask = cv2.inRange(Gimage,Glower,Gupper)
        Bmask = cv2.inRange(image,Blower,Bupper)

        # find contours in the threshold image
        image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gimage, Gcontours,Ghierarchy = cv2.findContours(Gthresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        masktest=cv2.imread('mask320.png',0)
        res = cv2.bitwise_and(image,image,mask=masktest)
        Gres = cv2.bitwise_and(Gimage,Gimage,mask=masktest)
        
        res, Rcontours,Rhierarchy = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gres, GRcontours,GRhierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        # finding contour with maximum area and store it as best_cnt - Black Area
        max_area = 0
        best_cnt = 1
        for cnt in Rcontours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
        
        # finding contour with maximum area and store it as best_cnt - Green Area
        max_area = 1000
        best_cnt = 1
        for cnt in GRcontours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        gx,gy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(blur,(gx,gy),10,(0,255,255),-1)
        
        # finding contour with maximum area and store it as best_cnt - Rescue Area
        max_area = 7000
        best_cnt = 1
        for cnt in GRcontours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        rx,ry = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(blur,(rx,ry),10,(255,0,255),-1)
        cv2.circle(blur,(170,170),10,(0,255,0),-1)
        print("x:{} y:{}".format(cx,cy))
        
        # show the frame
        cv2.imshow("setting",image) 
        cv2.imshow("Frame", blur)
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

