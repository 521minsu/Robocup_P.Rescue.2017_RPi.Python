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
SearchPlatform = False
Victimloc = 0

import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
cc = dc_motors.Motor.cameracontrol

# Check these before running
#######################################
motor_ENABLE = True                   #
#######################################
array_ENABLE = True                 #
#######################################
green_ENABLE = True                   #
#######################################
waterTower_ENABLE = False             #
WTLimit = 1                           #
#######################################
WTDone = 0

bx,bx1,bx2,by,gx,gy,rx,ry = 0,0,0,0,0,0,0,0
gx_high,gx_low = 200,150

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (128, 80)
camera.framerate = 50
camera.hflip = True

cc(cc,'down')
dc(dc,0,0)
lc(lc,'idle','release')

rawCapture = PiRGBArray(camera, size=(128, 80))

# allow the camera to warmup
time.sleep(1)
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):      
        #Make sure You are putting calibrated values in
        Min_BB,Min_BG,Min_BR,Max_BB,Max_BG,Max_BR = 0,0,0,255,50,255
        
        Min_GH,Min_GS,Min_GV,Max_GH,Max_GS,Max_GV = 40,30,60,80,170,190       #21,63,54        
        
        Min_VB,Min_VG,Min_VR,Max_VB,Max_VG,Max_VR = 0,0,0,255,245,255
        
        Min_OH,Min_OS,Min_OV,Max_OH,Max_OS,Max_OV = 150,110,110,195,195,195    #120,60,60
        
        
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
                by += 10
                cv2.circle(blur,(bx,by),5,(0,0,255),-1)      # Red Dot
            if bbx != 0:
                bby += 50
                cv2.circle(blur,(bbx,bby),5,(0,0,255),-1)      # Red Dot
            cv2.circle(blur,(170,160),5,(0,255,0),-1)    # Green Dot
            lineerror,turnerror = 1000,1000
            
            for i in range(3):
                dist = SR.value('distance')
            rescue_detection = 0
            
        #============== Search Victim ===================
            error = bx - bbx
            print("Threshold:  error:{} gx:{} \t gy:{}\t bx:{} \t bbx:{} \t dist:{}".format(error,gx,gy,bx,bbx,dist))
         
            if gx_low < gx < gx_high and bx == 0:
                print("Rescue starting")
                dc(dc,80,80)
                time.sleep(0.3)
                dc(dc,0,0)
                cc(cc,'up')
                time.sleep(1)
            
                Rescue_start = True

        #===================================================
                    
##            if gx == 0:
##                if bx != 0:
##                    bx2 = bx1
##                    bx1 = bx
##                    print("line dots check bx1:{} \t bx2:{}".format(bx1,bx2))
##                elif bx == 0:
##                    bxdiff = bx1 - bx2
##                    bx = bx1 + bxdiff
##                    # excute the calibrated - newly added
####                    Caliberror = bx - 160
####                    print("Calibrated bx:{} \t Caliberror:{} \t bx1:{} \t bx2:{}".format(bx,Caliberror,bx1,bx2))
##                    startTime = round(time.time())
##                    #Mainloop.linetrace(Mainloop,Caliberror,Kp,Ki,Kd,startTime)
            if bx != 0 and motor_ENABLE == True:  
                Kp,Ki,Kd = 47,15,10
                #lineerror = bbx - 160
                lineerror = bx - 160
                startTime = round(time.time())
                Mainloop.linetrace(Mainloop,lineerror,Kp,Ki,Kd,startTime)
            elif bx == 0 and array_ENABLE == True and motor_ENABLE == True:
                Mainloop.noblack()
            if gx != 0 and bbx != 0 and motor_ENABLE == True and green_ENABLE == True:
                turnerror = gx - bbx
                Mainloop.greenturn(Mainloop,turnerror)
            if waterTower_ENABLE == True and WTDone < WTLimit and dist < 20:
                print("Initializing Water Tower...")
                WaterTowerRun()
                
                  
            cv2.imshow("result",blur)
            
        if Rescue_start == True:
            Vimage = image
            Oimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
            
            Vlower = np.array([Min_VB,Min_VG,Min_VR],dtype="uint8")
            Vupper = np.array([Max_VB,Max_VG,Max_VR],dtype="uint8")
            
            Olower = np.array([Min_OH,Min_OS,Min_OV],dtype="uint8")
            Oupper = np.array([Max_OH,Max_OS,Max_OV],dtype="uint8")
            
            # Pure Masked image without any limits on its vision
            Vmask = cv2.inRange(Vimage,Vlower,Vupper)
            thresh,VmaskInv = cv2.threshold(Vmask,127,255,cv2.THRESH_BINARY_INV)
            Vres = VmaskInv[:,30:50]

            Omask = cv2.inRange(Oimage,Olower,Oupper)
            Ores = Omask[:,30:50]
            
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
            Omin_area = 300 # Was 530 before
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
                print("Victim detected... dist:{} vx:{} vy:{}".format(dist,vx,vy))
            if ox != 0 or oy != 0:
                ox += 30
                cv2.circle(Oimage,(ox,oy),5,(255,255,0),-1)
                print("Platform detected... dist:{} ox:{} oy:{}".format(dist,ox,oy))
            
##            cv2.imshow("Rescue",image)
##            cv2.imshow("Omask",Omask)
##            cv2.imshow("Ores",Ores)
##            cv2.imshow("Vmask",VmaskInv)
            
            dist = SR.value('distance')
            print("In rescue... dist:{} ox:{} vx:{} SearchPlatform:{}".format(dist,ox,vx,SearchPlatform))

            if vx != 0 and SearchPlatform == False:
                print("Initiallizing catchVictim Sequence... dist:{} \t ox:{}".format(dist,ox))
                while dist > 6:
                    dc(dc,100,100)
                    dist = SR.value('distance')
                    print("Approaching Victim... dist:{}".format(dist))
                # Travels forward for 0.5 more seconds to make sure it is possible to catch the victim
##                dc(dc,100,100)
##                time.sleep(0.2)
                # Controls the lifting mechanism in order to catch and lift the victim up
                dc(dc,0,0)
                lc(lc,'idle','catch')
                print("From catchVictim... the victim catched... dist:{}".format(dist))
                time.sleep(1.5)
                lc(lc,'lift','catch')
                time.sleep(1.5)
                dc(dc,-100,-100)
                time.sleep(0.5)
                dc(dc,0,0)
                first = True
                SearchPlatform = True
                print("From catchVictim... the victim lifted...")
                
            dist = SR.value('distance')
    ##        print("In rescue... dist:{} ox:{}".format(dist,ox))
            if first == True:
                for i in range(100):
                    dist = SR.value('distance')
                    print("Running for loop... i:{} \t dist:{}".format(i,dist))
                first = False
            
            if ox != 0 and SearchPlatform == True:
                while dist > 6:
                    dc(dc,100,100)
                    dist = SR.value('distance')
                    print("Approaching Platform... dist:{} ox:{}".format(dist,ox))
                # Travels forward for 0.5 more seconds to make sure it is possible to catch the victim
##                dc(dc,100,100)
##                time.sleep(0.3)
                dc(dc,0,0)
                lc(lc,'idle','catch')
                time.sleep(1)
                lc(lc,'idle','release')
                dc(dc,0,0)
                time.sleep(1)
                dc(dc,-100,-100)
                time.sleep(0.5)
                dc(dc,0,0)
                print("Releasing the victim... Finishing...")
                cv2.destroyAllWindows()
                break
            
            if SearchPlatform == False:
                if Victimloc == 0:
                    dc(dc,-80,80)
                elif Victimloc == 1:
                    dc(dc,80,-80)
            elif SearchPlatform == True:
                if Victimloc == 0:
                    dc(dc,80,-80)
                elif Victimloc == 1:
                    dc(dc,-80,80)
            

        
        key = cv2.waitKey(1) & 0xFF
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

except KeyboardInterrupt:
    dc_motors.Motor.cleanup(dc_motors)
    cv2.destroyAllWindows()
    
def WaterTowerRun():
    dc(dc,0,0)
    dc(dc,100,-100)
    time.sleep(0.5)
    dc(dc,100,100)
    time.sleep(0.2)
    dc(dc,20,100)
    time.sleep(2)
    print("_______________Finished Water Tower...")
    WTDone += 1
