# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 50
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(320, 240))

fgbg = cv2.createBackgroundSubtractorMOG2()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        image = frame.array
        
        fgmask = fgbg.apply(image)
        
        cv2.imshow('original',image)
        cv2.imshow('frame',fgmask)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)

