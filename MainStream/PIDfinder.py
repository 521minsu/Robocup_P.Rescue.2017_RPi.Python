#Camera & Opencv related modules
from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np

import time
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
cc = dc_motors.Motor.cameracontrol
bx,bx1,bx2,by,gx,gy,rx,ry = 0,0,0,0,0,0,0,0
gx_high,gx_low = 200,150

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (128, 80)
camera.framerate = 50
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(128, 80))

# allow the camera to warmup
time.sleep(1)
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):      
        #Make sure You are putting calibrated values in
        Min_BB,Min_BG,Min_BR,Max_BB,Max_BG,Max_BR = 0,0,0,255,70,255
        
        Min_GH,Min_GS,Min_GV,Max_GH,Max_GS,Max_GV = 20,50,70,80,160,180       #21,63,54        
        
        Min_VB,Min_VG,Min_VR,Max_VB,Max_VG,Max_VR = 0,0,0,255,225,255
        
        Min_OH,Min_OS,Min_OV,Max_OH,Max_OS,Max_OV = 0,110,100,20,215,255    #120,60,60
        
        
        # image from the Picam
        original = frame.array
        image = cv2.flip(original,0)
        
        #########################################
        #   Finding contours for line tracing   #
        #########################################
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

        Bres = Bmask[10:30]
        BBres = Bmask[50:70]
        Gres = Gmask[50:70]
        
        Bres, Rcontours,Rhierarchy = cv2.findContours(Bres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        BBres, BRcontours,BRhierarchy = cv2.findContours(BBres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gres, Gcontours,Ghierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
           
        # finding contour with maximum area and store it as best_cnt - Black Area
        # min_area = 1000
        Bmin_area = 300   
        Bbest_cnt = 1
        for Bcnt in Rcontours:
                Barea = cv2.contourArea(Bcnt)
                if Barea > Bmin_area:
                        Bmin_area = Barea
                        Bbest_cnt = Bcnt
        # finding centroids of best_cnt and draw a circle there
        BM = cv2.moments(Bbest_cnt)
        # cx, cy = black line following red dot
        bx,by = int(BM['m10']/BM['m00']), int(BM['m01']/BM['m00'])
        
        # finding contour with maximum area and store it as best_cnt - Black Area
        # min_area = 1000
        BBmin_area = 300    
        BBbest_cnt = 1
        for BBcnt in BRcontours:
                BBarea = cv2.contourArea(BBcnt)
                if BBarea > BBmin_area:
                        BBmin_area = BBarea
                        BBbest_cnt = BBcnt
        # finding centroids of best_cnt and draw a circle there
        BBM = cv2.moments(BBbest_cnt)
        # cx, cy = black line following red dot
        bbx,bby = int(BBM['m10']/BBM['m00']), int(BBM['m01']/BBM['m00'])
        
        # finding contour with maximum area and store it as best_cnt - Green Area
        Gmin_area = 100 # Was 530 before
        Gbest_cnt = 1
        for Gcnt in Gcontours:
                Garea = cv2.contourArea(Gcnt)
                if Garea > Gmin_area:
                        Gmin_area = Garea
                        Gbest_cnt = Gcnt
        # finding centroids of best_cnt and draw a circle there
        GM = cv2.moments(Gbest_cnt)
        # gx, gy = green area following yellow dot
        gx,gy = int(GM['m10']/GM['m00']), int(GM['m01']/GM['m00'])        
        
        # green dot where the middle line of the video feed is
        if gx != 0:
            gy += 50
            cv2.circle(blur,(gx,gy),5,(255,0,0),-1)      # Blue Dot
        if bx != 0:
            by += 20
            cv2.circle(blur,(bx,by),5,(0,0,255),-1)      # Red Dot
        if bbx != 0:
            bby += 150
            cv2.circle(blur,(bbx,bby),5,(0,0,255),-1)      # Red Dot
        cv2.circle(blur,(170,160),5,(0,255,0),-1)    # Green Dot
        lineerror,turnerror = 1000,1000
       
    #============== Search Victim ===================
        
##        if gx == 0:
##            if bx != 0:
##                bx2 = bx1
##                bx1 = bx
##                print("line dots check bx1:{} \t bx2:{}".format(bx1,bx2))
##            elif bx == 0:
##                bxdiff = bx1 - bx2
##                bx = bx1 + bxdiff
##                # excute the calibrated - newly added
##    ##                    Caliberror = bx - 160
##    ##                    print("Calibrated bx:{} \t Caliberror:{} \t bx1:{} \t bx2:{}".format(bx,Caliberror,bx1,bx2))
##                startTime = round(time.time())
##                #Mainloop.linetrace(Mainloop,Caliberror,Kp,Ki,Kd,startTime)
        
        if bx == 0:
            array = SR.value('IRArray')
            Lspeed,Rspeed = 0,0
            if array == 2:
                Lspeed,Rspeed = -100,100
            elif array == 4:
                Lspeed,Rspeed = -90,100
            elif array == 8:
                Lspeed,Rspeed = 100,100
            elif array == 16:
                Lspeed,Rspeed = 100,-90
            elif array == 32:
                Lspeed,Rspeed = 100,-100
            elif array == 6:
                Lspeed,Rspeed = -90,100
            elif array == 14:
                Lspeed,Rspeed = -100,100
            elif array == 12:
                Lspeed,Rspeed = -90,100
            elif array == 28:
                Lspeed,Rspeed = 100,100
            elif array == 24:
                Lspeed,Rspeed = 100,-90
            elif array == 56:
                Lspeed,Rspeed = 100,-100
            elif array == 48:
                Lspeed,Rspeed = 100,-90
            elif array == 60:
                Lspeed,Rspeed = 100,-100
            elif array == 30:
                Lspeed,Rspeed = -100,100
            print("There was NO black detected... array:{} \t Lspeed:{} \t Rspeed:{}".format(array,Lspeed,Rspeed))
            dc(dc,Lspeed,Rspeed)
                
        mSpeed = 100
        integral,derivative,lasterror = 0,0,0
        pidturn = 0
       
        Kp,Ki,Kd = 77,30,17
        error = 64 - bx
        startTime = round(time.time())
        
        integral += error
        derivative = error - lasterror
        pidturn = Kp*error + Ki*integral + Kd*derivative
        pidturn = pidturn/100
        lasterror = error
        
        print("Threshold:  error:{} gx:{} \t gy:{}\t bx:{} \t bbx:{} \t ".format(error,gx,gy,bx,bbx))
        
        Lspeed,Rspeed = mSpeed+pidturn, mSpeed-pidturn
        if Lspeed > 90:
            Lspeed = 90
        elif Lspeed < -90:
            Lspeed = -90
        if Rspeed > 90:
            Rspeed = 90
        elif Rspeed < -80:
            Rspeed = -80
        curTime = round(time.time())
        timePassed = curTime - startTime
        print("ERROR:{} \t pidturn:{} time:{} \t Ls:{} \t Rspeed:{}".format(error,pidturn,timePassed,Lspeed,Rspeed))
        dc(dc,Lspeed,Rspeed)
              
        cv2.imshow("result",blur)

        key = cv2.waitKey(1) & 0xFF
            
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
except:
    print("Passed an error from PIDfinder.py")
    dc_motors.Motor.cleanup(dc_motors)
    cv2.destroyAllWindows() 
