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
from copy import copy
import time
import cv2
import numpy as np

#Loop and program related modules
from Loop import MainControl as Mainloop
import SensorReading as SR
import rescue
Rescue = False
CatchIt = False
finished = False

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

# initialize the camera and grab a reference to the raw camera capture
cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
cap.set(15,1)

cc(cc,'down')
 
# allow the camera to warmup
time.sleep(5)

# capture frames from the camera
while True:      
      if Rescue == False:
          # image from the Picam
          ret,image = cap.read()
          # images from the Picam with filters and effects
          Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
          blur = cv2.blur(image, (3,3))
          
          Min_BB,Min_BG,Min_BR = 0,0,0
          Max_BB,Max_BG,Max_BR = 255,86,255
          
          Min_GH,Min_GS,Min_GV = 27,43,13
          Max_GH,Max_GS,Max_GV = 76,170,165
          
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
          min_area = 530
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
          
          # Gets the distance Value, but reads 5 times so there's no typeError when going through rest of the program
          for i in range(0,5):
              dist = SR.value('distance')
          
          
          if bx != 0 and motor_ENABLE == True:
              lineerror = bx - 170
              Mainloop.linetrace(Mainloop,lineerror)
              print("From Main.py Black... obstacle:{}cm".format(dist))
          if gx != 0 and bx != 0 and motor_ENABLE == True and green_ENABLE == True:
              turnerror = gx - bx
              Mainloop.greenturn(Mainloop,turnerror)
          if waterTower_ENABLE == True and WTDone < WTLimit:
              Mainloop.watertower(Mainloop,dist)
              WTDone += 1
              print("From Main.py WT... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t obstacle:{}cm".format(lineerror,bx,by,gx,gy,dist))
          elif WTDone >= WTLimit:
              if rx != 0 and bx == 0 and dist <= 60:
                  dc(dc,0,0)
                  print("From Main.py rescue_init... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t obstacle:{}cm".format(lineerror,bx,by,gx,gy,dist))
                  cc(cc,'up')
                  time.sleep(1)
                  startTime = round(time.time())
                  timePassed = 0
                  victimFound = 0
                  searchDir = 0
                  Rescue = True
          else:
              print("From Main.py else... error:{} \t bx:{} \t by:{} \t gx:{} \t gy:{} \t distance:{}cm".format(lineerror,bx,by,gx,gy,dist))
          
          cv2.imshow("result",blur)
          #cv2.imshow("Gmask",Gmask)
          #cv2.imshow("Gres",Gres)
          #cv2.imshow("Bmask",Bmask)
          #cv2.imshow("Bres",res)
          
          key = cv2.waitKey(1) & 0xFF
      
          print(dist)
      
      ##############################################################################
      #  !!!!!!!!!!!!!!!!!!!! Rescue is True from here !!!!!!!!!!!!!!!!!!!!!!!!!!  #
      ##############################################################################
            
      elif Rescue == True:
          # image from the Picam
          image = cap.read()
          # images from the Picam with filters and effects
          Rimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
          blur = cv2.blur(image, (3,3))
          
          Min_OH,Min_OS,Min_OV = 156,89,82        #Please put in the calibrated values
          Max_OH,Max_OS,Max_OV = 220,255,255
          
          #Please Run Calibration.py first, and bring back the values according to the current situation
          Olower = np.array([Min_OH,Min_OS,Min_OV],dtype="uint8")
          Oupper = np.array([Max_OH,Max_OS,Max_OV],dtype="uint8")
          
          Rmask = cv2.inRange(Rimage,Olower,Oupper)
          
          resvisionmask=cv2.imread('rescue_mask.png',0)
          Rres = cv2.bitwise_and(Rmask,Rmask,mask=resvisionmask)
          
          Rres, Rcontours,Rhierarchy = cv2.findContours(Rres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
          
          # finding contour with maximum area and store it as best_cnt - Rescue Area
          min_area = 255
          best_cnt = 1
          for cnt in Rcontours:
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
          cv2.circle(blur,(60,160),5,(0,255,0),-1)
          
          for i in range(0,5):
              dist = SR.value('distance')
          
          
          if dist <= 40 and rx == 0 and ry == 0:
              CatchIt = True
              break
          
          cv2.imshow("result",blur)
          cv2.imshow("Rmask",Rmask)
          cv2.imshow("Rres",Rres)
          print("distance:{}".format(dist))
          
          key = cv2.waitKey(1) & 0xFF

          curTime = round(time.time())
          timePassed = curTime - startTime

          if timePassed >= 2:
              if searchDir == 0: # Converting from Left to Right
                  searchDir = 1
              elif searchDir == 1: # Converting from RIght to Left
                  searchDir = 0
              startTime = round(time.time())

          if searchDir == 0:
              dc(dc,-50,50)
          elif searchDir == 1:
              dc(dc,50,-50)

          # if the `q` key was pressed, break from the loop
          if key == ord("q"):
              cv2.destroyAllWindows()
              break
              
if CatchIt == True:
    rescue.catchVictim()

