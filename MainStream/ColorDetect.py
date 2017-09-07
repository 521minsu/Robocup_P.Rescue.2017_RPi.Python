######################################
#  Robocup_Junior_2017_Premier_Main  #
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 08.08.17             #
######################################

##############################################
# !!!!!!! Color Detecting Test Code !!!!!!! #
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

Rescue_start = True
SearchPlatform = False

import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
cc = dc_motors.Motor.cameracontrol

# Check these before running
#######################################
motor_ENABLE = True                   #
#######################################

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
        if vx != 0 :
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
        
        
        dc(dc,-75,75)
        

    
    key = cv2.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
