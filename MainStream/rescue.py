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

###From Detector.py
detector=cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread("detectionTest.png",0)
trainKP,trainDesc=detector.detectAndCompute(trainImg,None)
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (256, 144)
camera.framerate = 30
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(256, 144))
 
# allow the camera to warmup
time.sleep(0.1)

def nothing(x):
    pass

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        curr_img = frame.array
        image = curr_img

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
            trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
            queryBorder=cv2.perspectiveTransform(trainBorder,H)
            cv2.polylines(image,[np.int32(queryBorder)],True,(0,255,0),5)
            print("Image Detected")
            cv2.imshow('result',image)
        else:
            print ("Not Enough match found- {}/{}".format(len(goodMatch),MIN_MATCH_COUNT))
            cv2.imshow('result',image)           
        
        
        #cv2.imshow('thresh',thresh2)
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
