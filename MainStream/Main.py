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

Rescue_start = False
SearchPlatform = False

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
gx_high,gx_low = 200,150

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = False

cc(cc,'down')
dc(dc,0,0)
lc(lc,'idle','release')

rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):      
    #Make sure You are putting calibrated values in
    Min_BB,Min_BG,Min_BR = 0,0,0
    Max_BB,Max_BG,Max_BR = 255,47,255
        
    Min_GH,Min_GS,Min_GV = 21,63,54
    Max_GH,Max_GS,Max_GV = 80,196,197
    
    Min_VB,Min_VG,Min_VR = 0,0,0
    Max_VB,Max_VG,Max_VR = 255,228,255
        
    Min_OH,Min_OS,Min_OV = 150,20,70
    Max_OH,Max_OS,Max_OV = 170,110,120
    
    if Rescue_start == False:
        #########################################
        #   Finding contours for line tracing   #
        #########################################
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

        Bres = Bmask[30:90]
        Gres = Gmask[150:210]
        GRres = Gmask[0:30]
        
        Bres, Rcontours,Rhierarchy = cv2.findContours(Bres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Gres, Gcontours,Ghierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        GRres, GRcontours,GRhierarchy = cv2.findContours(GRres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
        # finding contour with maximum area and store it as best_cnt - Black Area
        # min_area = 1000
        Bmin_area = 1000    
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
        
        # finding contour with maximum area and store it as best_cnt - Green Area
        Gmin_area = 1000 # Was 530 before
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
        
        # finding contour with maximum area and store it as best_cnt - Green Rescue Area
        min_area = 9200
        best_cnt = 1
        for cnt in GRcontours:
                area = cv2.contourArea(cnt)
                if area > min_area:
                        min_area = area
                        best_cnt = cnt
        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        # gx, gy = green area following yellow dot
        grx,gry = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        
        
        # green dot where the middle line of the video feed is
        if gx != 0:
            gy = gy + 150
            cv2.circle(blur,(gx,gy),5,(255,0,0),-1)      # Blue Dot
        if bx != 0:
            by = by + 30
            cv2.circle(blur,(bx,by),5,(0,0,255),-1)      # Red Dot
        cv2.circle(blur,(170,160),5,(0,255,0),-1)    # Green Dot
        lineerror,turnerror = 1000,1000
        
        # Gets the distance Value, but reads 5 times so there's no typeError when going through rest of the program
        for i in range(5):
            dist = SR.value('distance')
        rescue_detection = 0
        
    #============== Search Victim ===================
        print("Threshold..:   gx:{} \t gy:{}\t bx:{} \t by:{}".format(gx,gy,bx,by))
     
        if gx_low < gx < gx_high and bx == 0:
            print("Rescue starting")
            dc(dc,100,100)
            time.sleep(1)
            dc(dc,0,0)
            cc(cc,'up')
            time.sleep(1)
        
            Rescue_start = True

    #===================================================
                
                
        if bx != 0 and motor_ENABLE == True:
            lineerror = bx - 170
            Mainloop.linetrace(Mainloop,lineerror)
            #print("From Main.py Black... obstacle:{}cm".format(dist))
        if gx != 0 and bx != 0 and motor_ENABLE == True and green_ENABLE == True:
            turnerror = gx - bx
            Mainloop.greenturn(Mainloop,turnerror)
        if waterTower_ENABLE == True and WTDone < WTLimit:
            Mainloop.watertower(Mainloop,dist)
            WTDone += 1
            #print("From Main.py WT... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t obstacle:{}cm".format(lineerror,bx,by,gx,gy,dist))
        #else:
            #print("From Main.py else... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t distance:{}cm".format(lineerror,bx,by,gx,gy,dist))
        
            
              
        #cv2.imshow("result",blur)
        #cv2.imshow("Gmask",Gmask)
        #cv2.imshow("Gres",Gres)
        #cv2.imshow("Bmask",Bmask)
        #cv2.imshow("Bres",res)
        
    if Rescue_start == True:
        original = frame.array
        hflip = cv2.flip(original,1)
        image = cv2.flip(hflip,0)
        Vimage = image
        Oimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        
        Vlower = np.array([Min_VB,Min_VG,Min_VR],dtype="uint8")
        Vupper = np.array([Max_VB,Max_VG,Max_VR],dtype="uint8")
        
        Olower = np.array([Min_OH,Min_OS,Min_OV],dtype="uint8")
        Oupper = np.array([Max_OH,Max_OS,Max_OV],dtype="uint8")
        
        # Pure Masked image without any limits on its vision
        Vmask = cv2.inRange(Vimage,Vlower,Vupper)
        thresh,VmaskInv = cv2.threshold(Vmask,127,255,cv2.THRESH_BINARY_INV)
        Vres = VmaskInv[:,125:195]

        Omask = cv2.inRange(Oimage,Olower,Oupper)
        Ores = Omask[:,125:195]
        
        Vres, Vcontours,Vhierarchy = cv2.findContours(Vres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        Ores, Ocontours,Ohierarchy = cv2.findContours(Ores,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        # finding contour with maximum area and store it as best_cnt - Green Area
        Vmin_area = 50 # Was 530 before
        Vbest_cnt = 1
        for Vcnt in Vcontours:
                Varea = cv2.contourArea(Vcnt)
                if Varea > Vmin_area:
                        Vmin_area = Varea
                        Vbest_cnt = Vcnt
        # finding centroids of best_cnt and draw a circle there
        VM = cv2.moments(Vbest_cnt)
        vx,vy = int(VM['m10']/VM['m00']), int(VM['m01']/VM['m00'])
        
        # finding contour with maximum area and store it as best_cnt - Green Are
        Omin_area = 1500 # Was 530 before
        Obest_cnt = 1
        for Ocnt in Ocontours:
                Oarea = cv2.contourArea(Ocnt)
                if Oarea > Omin_area:
                        Omin_area = Oarea
                        Obest_cnt = Ocnt
        # finding centroids of best_cnt and draw a circle there
        OM = cv2.moments(Obest_cnt)
        ox,oy = int(OM['m10']/OM['m00']), int(OM['m01']/OM['m00'])
        
        
        # green dot where the middle line of the video feed is
        #if vx != 0 or vy != 0:
        if vx != 0 and SearchPlatform == False:
            vx += 125
            cv2.circle(Oimage,(vx,vy),5,(255,0,0),-1)      # Blue Dot
            print("Victim detected... dist:{} vx:{} vy:{}".format(dist,vx,vy))
        if ox != 0 or oy != 0:
            ox += 125
            cv2.circle(Oimage,(ox,oy),5,(255,255,0),-1)
            print("Platform detected... dist:{} ox:{} oy:{}".format(dist,ox,oy))
        
        cv2.imshow("Rescue",image)
        cv2.imshow("Omask",Ores)
        cv2.imshow("Vmask",VmaskInv)
        
        dist = SR.value('distance')
        print("In rescue... dist:{} ox:{} vx:{} SearchPlatform:{}".format(dist,ox,vx,SearchPlatform))
            
        if vx != 0 and SearchPlatform == False:
            print("Initiallizing catchVictim Sequence... dist:{} \t ox:{}".format(dist,ox))
            while dist > 9:
                dc(dc,100,100)
                dist = SR.value('distance')
                print("Approaching Victim... dist:{}".format(dist))
            # Travels forward for 0.5 more seconds to make sure it is possible to catch the victim
            dc(dc,100,100)
            time.sleep(0.5)
            # Controls the lifting mechanism in order to catch and lift the victim up
            dc(dc,0,0)
            lc(lc,'idle','catch')
            print("From catchVictim... the victim catched... dist:{}".format(dist))
            time.sleep(1.5)
            lc(lc,'lift','catch')
            time.sleep(1.5)
            dc(dc,-100,-100)
            time.sleep(1)
            dc(dc,0,0)
            SearchPlatform = True
            print("From catchVictim... the victim lifted...")
            
        #dist = SR.value('distance')
        #print("In rescue... dist:{} ox:{}".format(dist,ox))
        
        if ox != 0 and SearchPlatform == True:
            while dist > 9:
                dc(dc,100,100)
                dist = SR.value('distance')
                print("Approaching Platform... dist:{} ox:{}".format(dist,ox))
            # Travels forward for 0.5 more seconds to make sure it is possible to catch the victim
            dc(dc,100,100)
            time.sleep(0.5)
            cv2.imshow("Omask1",Omask)
            dc(dc,0,0)
            lc(lc,'idle','release')
            dc(dc,-100,-100)
            time.sleep(0.5)
            dc(dc,0,0)
            print("Releasing the victim... Finishing...")
##            cv2.destroyAllWindows()
            break
        
        
        dc(dc,-75,75)
        

    
    key = cv2.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)


