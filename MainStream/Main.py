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

#import rescue
Rescue = False

## Enabling SIFT module
detector=cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread("images/victim.jpg",0)

trainKP,trainDesc=detector.detectAndCompute(trainImg,None)

finished = False

def nothing(x):
    pass

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
MIN_MATCH_COUNT=10                    #
#######################################

WTDone = 0

bx,by,gx,gy,rx,ry = 0,0,0,0,0,0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = False

cc(cc,'down')

rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(1)


def catchVictim():
    dist = SR.value('distance')
    # Catches the victim after finding it
    while dist > 7:
        dc(dc,100,100)
    # Travels forward for 0.5 more seconds to make sure it is possible to catch the victim
    dc(dc,100,100)
    time.sleep(0.5)
    # Controls the lifting mechanism in order to catch and lift the victim up
    dc(dc,0,0)
    lc(lc,'idle','catch')
    time.sleep(0.5)
    lc(lc,'lift','catch')
    time.sleep(0.5)
    # Calls the searchPlatform function and searches for the platform
    searchPlatform()


def searchPlatform():
    dist = SR.value('distance')
    startTime = round(time.time())
    searchDir = 0
    
    while dist > 25:
        dist = SR.value('distance')
        
        curTime = round(time.time())
        TimePassed = curTime - startTime
        
        if TimePassed >= 2:
            if searchDir == 0:
                searchDir = 1
            elif searchDir == 1:
                searchDir = 0
            
            startTime = round(time.time())
        
        if searchDir == 0:
            dc(dc,-50,50)
        elif searchDir == 1:
            dc(dc,50,-50)
    
    dc(dc,0,0)
    print("Platform Found... Entering the Final Phrase...")
    placeAndFinish()
    
def placeAndFinish():
    dist = SR.value('distance')
    
    while dist > 10:
        dc(dc,100,100)
    dc(dc,100,100)
    time.sleep(0.5)
    dc(dc,0,0)
    
    lc(lc,'idle','release')
    
    dc(dc,-100,-100)
    time.sleep(2)
    dc(dc,0,0)
    finished = True
    
    
class Finished(Exception):
    '''The program has reached its end'''


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      if Rescue == False:
          # image from the Picam
          image = frame.array
          # images from the Picam with filters and effects
          Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
          blur = cv2.blur(image, (3,3))
          
          Min_BB,Min_BG,Min_BR = 0,0,0
          Max_BB,Max_BG,Max_BR = 255,50,255
          
          Min_GH,Min_GS,Min_GV = 24,0,38
          Max_GH,Max_GS,Max_GV = 85,255,255
          
          #Please Run Calibration.py first, and bring back the values according to the current situation
          Blower = np.array([Min_BB,Min_BG,Min_BR],dtype="uint8")
          Bupper = np.array([Max_BB,Max_BG,Max_BR],dtype="uint8")
          #Please Run Calibration.py first, and bring back the values according to the current situation
          Glower = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8")
          Gupper = np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
          
          Gmask = cv2.inRange(Gimage,Glower,Gupper)
          Bmask = cv2.inRange(image,Blower,Bupper)
          
          # find contours in the threshold image
          image, contours,hierarchy = cv2.findContours(Bmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
          Gimage, GRcontours,GRhierarchy = cv2.findContours(Gmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
          
          visionmask=cv2.imread('mask_noside.png',0)
          res = cv2.bitwise_and(Bmask,Bmask,mask=visionmask)
          Gres = cv2.bitwise_and(Gmask,Gmask,mask=visionmask)
          
          res, Rcontours,Rhierarchy = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
          Gres, Gcontours,Ghierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
              
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
          bx,by = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
          
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
          # gx, gy = green area following yellow dot
          gx,gy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
          
          # finding contour with maximum area and store it as best_cnt - Rescue Area
          min_area = 5000
          best_cnt = 1
          for cnt in GRcontours:
                  area = cv2.contourArea(cnt)
                  if area > min_area:
                          min_area = area
                          best_cnt = cnt
          
          # finding centroids of best_cnt and draw a circle there
          M = cv2.moments(best_cnt)
          # rx, ry = Pink dot when Rescue has been reached.
          rx,ry = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
          
          
          # green dot where the middle line of the video feed is
          cv2.circle(blur,(rx,ry),5,(255,255,0),-1)
          cv2.circle(blur,(gx,gy),5,(255,0,0),-1)
          cv2.circle(blur,(bx,by),5,(0,0,255),-1)
          cv2.circle(blur,(170,160),5,(0,255,0),-1)
          lineerror,turnerror = 1000,1000
          
          if bx != 0 and motor_ENABLE == True:
              lineerror = bx - 170
              Mainloop.linetrace(Mainloop,lineerror)
          if gx != 0 and bx != 0 and motor_ENABLE == True and green_ENABLE == True:
              turnerror = gx - bx
              Mainloop.greenturn(Mainloop,turnerror)
          if waterTower_ENABLE == True and WTDone < WTLimit:
              dist = SR.value('distance')
              Mainloop.watertower(Mainloop,dist)
              WTDone += 1
              print("From Main.py ... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t obstacle:{}cm".format(lineerror,bx,by,gx,gy,dist))
          elif WTDone >= WTLimit:
              dist = SR.value('distance')
              if rx != 0 and bx == 0 and dist <= 65:
                  dc(dc,0,0)
                  print("From Main.py ... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t obstacle:{}cm".format(lineerror,bx,by,gx,gy,dist))
                  cc(cc,'up')
                  startTime = round(time.time())
                  timePassed = 0
                  victimFound = 0
                  searchDir = 0
                  Rescue = True
          else:
              dist = SR.value('distance')
              print("From Main.py ... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t distance:{}cm".format(lineerror,bx,by,gx,gy,dist))
          
          cv2.imshow("result",blur)
          #cv2.imshow("Gmask",Gmask)
          #cv2.imshow("Gres",Gres)
          #cv2.imshow("Bmask",Bmask)
          #cv2.imshow("Bres",res)
          
          key = cv2.waitKey(1) & 0xFF
          
                    # clear the stream in preparation for the next frame
          rawCapture.truncate(0)
      
      elif Rescue == True:
            image = frame.array
            Rimage = image
            
##            rescue_visionmask = cv2.imread("images/object_detectionmask.png")
##            resmasked = cv2.bitwise_and(Rimage,Rimage,mask=rescue_visionmask)
            if finished == True:
                raise Finished

            queryKP,queryDesc=detector.detectAndCompute(image,None)
            matches=flann.knnMatch(queryDesc,trainDesc,k=2)

            goodMatch=[]
            for m,n in matches:
               if(m.distance<0.75*n.distance):
                   goodMatch.append(m)
            if(len(goodMatch)>MIN_MATCH_COUNT):
               tp=[]
               qp=[]
               for m in goodMatch:
                   tp.append(trainKP[m.trainIdx].pt)
                   qp.append(queryKP[m.queryIdx].pt)
               
               tp,qp=np.float32((tp,qp))
               H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
               h,w=trainImg.shape
               print("Image Detected... entering catchVictim Process")
               dc(dc,0,0)
               catchVictim()
               cv2.imshow('result',image)
            else:
               print ("Not Enough match found- {}/{}".format(len(goodMatch),MIN_MATCH_COUNT))
               cv2.imshow('result',image)           


            #cv2.imshow('thresh',thresh2)
            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            curTime = round(time.time())
            timePassed = curTime - startTime

            if timePassed == 2:
               if searchDir == 0: # Converting from Left to Right
                   searchDir = 1
               elif searchDir == 1: # Converting from RIght to Left
                   searchDir = 0
               startTime = round(time.time())

            if searchDir == 0:
               dc(dc,-75,75)
            elif searchDir == 1:
               dc(dc,75,-75)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
               cv2.destroyAllWindows()



      
                
