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

# motor related module
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol

# enable SURF feature in opencv 3.2.0
surf = cv2.xfeatures2d.SURF_create()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = False
rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)

# Read images from the directory
detection  = cv2.imread('detectTest.png',0)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      # image from the Picam
	    image = frame.array
      
        
