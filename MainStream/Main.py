######################################
#  Robocup_Junior_2017_Premier_Main  #
# ---------------------------------- # 
#  Description: This program detects #
#  colors and sends the results to   #
#  Loop.py in the same directory     #
# ---------------------------------- #
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 10.09.17             #
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

first = False
Rescue_start = False
Rescue_alert = 0
SearchPlatform = False
Victimloc = 0

import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
cc = dc_motors.Motor.cameracontrol

bx,bx1,bx2,by,gx,gy,rx,ry = 0,0,0,0,0,0,0,0
gx_high,gx_low = 84,44
oxa,vxa,Rescue_alert,greenturn = 0,0,0,0
debug = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (128, 80)
camera.framerate = 50
camera.hflip = True

cc(cc,'down')
dc(dc,0,0)
lc(lc,'idle','release')
time.sleep(1)
cc(cc,'stop')

rawCapture = PiRGBArray(camera, size=(128, 80))

# allow the camera to warmup
time.sleep(1)
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):      
        #Make sure You are putting calibrated values in
        Min_BB,Min_BG,Min_BR,Max_BB,Max_BG,Max_BR = 0,0,0,255,0,255
        
        Min_GH,Min_GS,Min_GV,Max_GH,Max_GS,Max_GV = 40,20,40,80,170,180       #21,63,54        
        
        Min_VB,Min_VG,Min_VR,Max_VB,Max_VG,Max_VR = 0,0,0,255,225,255
        
        Min_OH,Min_OS,Min_OV,Max_OH,Max_OS,Max_OV = 150,110,80,185,195,195    #120,60,60
        
        
        # image from the Picam
        original = frame.array
        image = cv2.flip(original,0)
        
        if Rescue_start == False:
            #########################################
            #   Finding contours for line tracing   #
            #########################################
            # images from the Picam with filters and effects
            Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
            blur = cv2.blur(image, (3,3))
            
            #Please Run Calibration.py first, and bring back the values according to the current situation
            Blower,Bupper = np.array([Min_BB,Min_BG,Min_BR],dtype="uint8"),np.array([Max_BB,Max_BG,Max_BR],dtype="uint8")
            #Please Run Calibration.py first, and bring back the values according to the current situation
            Glower,Gupper = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8"),np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
            
            # Pure Masked image without any limits on its vision
            Gmask,Bmask = cv2.inRange(Gimage,Glower,Gupper),cv2.inRange(image,Blower,Bupper)

            Bres,BBres,Gres = Bmask[10:30],Bmask[50:70],Gmask[50:70]
            
            Bres, Rcontours,Rhierarchy = cv2.findContours(Bres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            BBres, BRcontours,BRhierarchy = cv2.findContours(BBres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            Gres, Gcontours,Ghierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
               
            # finding contour with maximum area and store it as best_cnt - Black Area
            # min_area = 1000
            Bmin_area = 100    
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
            BBmin_area = 200    
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
                by += 10
                cv2.circle(blur,(bx,by),5,(0,0,255),-1)      # Red Dot
            if bbx != 0:
                bby += 50
                cv2.circle(blur,(bbx,bby),5,(0,0,255),-1)      # Red Dot
            cv2.circle(blur,(170,160),5,(0,255,0),-1)    # Green Dot
            lineerror,turnerror = 1000,1000
            
        #============== Search Victim ===================
            print("Threshold:  gx:{} \t gy:{}\t bx:{} \t bbx:{} \t debug:{}".format(gx,gy,bx,bbx,debug))
         
            if gx_low < gx < gx_high and bx == 0:
                print("Rescue starting")
                dc(dc,80,80)
                time.sleep(0.4)
                dc(dc,0,0)
                cc(cc,'up')
                lc(lc,'lift','idle')
                time.sleep(1)
                
                Rescue_alert = 1

            ###########################################################
            greenturn = 2
            if gx != 0 and bbx != 0:
                turnerror = gx - bbx
                if turnerror > 0:
                    greenturn = 1
                elif turnerror < 0:
                    greenturn = 0
                                
            toArduino = "G" + str(greenturn) + "R" + str(Rescue_alert) + "V" + str(0) + "O" + str(0) + "*"
            SR.write(toArduino)
            print("printed {} to Arduino... Main.py".format(toArduino))
            
            if Rescue_alert == 1:
                Rescue_start = True
            cv2.imshow("result",blur)
            
        if Rescue_start == True:
            Vimage,Oimage = image,cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
            
            Vlower,Vupper = np.array([Min_VB,Min_VG,Min_VR],dtype="uint8"),np.array([Max_VB,Max_VG,Max_VR],dtype="uint8")
            Olower,Oupper  = np.array([Min_OH,Min_OS,Min_OV],dtype="uint8"),np.array([Max_OH,Max_OS,Max_OV],dtype="uint8")
                        
            Vmask = cv2.inRange(Vimage,Vlower,Vupper)
            thresh,VmaskInv = cv2.threshold(Vmask,127,255,cv2.THRESH_BINARY_INV)
            Vres = VmaskInv[:,44:84]

            Omask = cv2.inRange(Oimage,Olower,Oupper)
            thresh,OmaskInv = cv2.threshold(Omask,127,255,cv2.THRESH_BINARY_INV)
            Ores = Omask[:,44:84]
            
            Vres, Vcontours,Vhierarchy = cv2.findContours(Vres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            Ores, Ocontours,Ohierarchy = cv2.findContours(Ores,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
            # finding contour with maximum area and store it as best_cnt - Green Area
            Vmin_area = 3 # Was 530 before
            Vbest_cnt = 1
            for Vcnt in Vcontours:
                    Varea = cv2.contourArea(Vcnt)
                    if Varea > Vmin_area:
                            Vmin_area = Varea
                            Vbest_cnt = Vcnt
            # finding centroids of best_cnt and draw a circle there
            VM = cv2.moments(Vbest_cnt)
            vx,vy = int(VM['m10']/VM['m00']), int(VM['m01']/VM['m00'])
            
            # finding contour with maximum area and store it as best_cnt - Orange Are
            Omin_area = 200 # Was 530 before
            Obest_cnt = 1
            for Ocnt in Ocontours:
                    Oarea = cv2.contourArea(Ocnt)
                    if Oarea > Omin_area:
                            Omin_area = Oarea
                            Obest_cnt = Ocnt
            # finding centroids of best_cnt and draw a circle there
            OM = cv2.moments(Obest_cnt)
            ox,oy = int(OM['m10']/OM['m00']), int(OM['m01']/OM['m00'])
            


            if vx != 0 and SearchPlatform == False:
                vx += 30
                cv2.circle(Oimage,(vx,vy),5,(255,0,0),-1)      # Blue Dot
                print("Victim detected... vx:{} vy:{}".format(vx,vy))
            if ox != 0 or oy != 0:
                ox += 30
                cv2.circle(Oimage,(ox,oy),5,(255,255,0),-1)
                print("Platform detected... ox:{} oy:{}".format(ox,oy))
            
            cv2.imshow("Rescue",image)
            cv2.imshow("Omask",Omask)
            cv2.imshow("Ores",Ores)
            cv2.imshow("Vmask",VmaskInv)
            
            if vx != 0:
                vxa = 1
            else:
                vxa = 0
            if ox != 0:
                oxa = 1
            else:
                oxa = 0
                
            toArduino = "G" + str(0) + "R" + str(1) + "V" + str(vxa) + "O" + str(oxa) + "*"
            SR.write(toArduino)
            print("Sending {} to Arduino... rescue \t debug:{}".format(toArduino,debug))
            
        debug += 1
        key = cv2.waitKey(1) & 0xFF
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

except KeyboardInterrupt:
    dc_motors.Motor.cleanup(dc_motors)
    cv2.destroyAllWindows()
    
