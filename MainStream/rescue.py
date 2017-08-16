########################################
#  Robocup_Junior_2017_Premier_Rescue  #
# ------------------------------------ # 
#  Description: This program controls  #
#  and directs the robot when it       #
#  has reached the rescue tile.        #
# ------------------------------------ #
#  Author: Minsu Kim                   #
#  Email : 521minsu@gmail.com          #
#  Last Update: 08.08.17               #
########################################

#Camera & Opencv related modules
from picamera.array import PiRGBArray
from picamera import PiCamera
from copy import copy
import time
import cv2
import numpy as np

#########################################
MIN_MATCH_COUNT=3
#########################################

# motor related module
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol


import SensorReading as SR

## Enabling SIFT module
detector=cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread("images/detectionTest.png",0)
trainKP,trainDesc=detector.detectAndCompute(trainImg,None)

finished = False
first = True

def nothing(x):
    pass
    
    
#####################################################################
def start(curr_img):
    if first == True:
        startTime = round(time.time())
        timePassed = 0
    
        victimFound = 0
        searchDir = 0
    else:
        image = curr_img

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
           dc(dc,-50,50)
        elif searchDir == 1:
           dc(dc,50,-50)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
           cv2.destroyAllWindows()



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