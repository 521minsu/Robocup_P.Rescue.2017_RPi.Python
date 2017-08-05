# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

MIN_MATCH_COUNT=5


###From Detector.py
detector=cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread("TrainingData/TrainImg.jpeg",0)
trainKP,trainDesc=detector.detectAndCompute(trainImg,None)
trainKP1,trainDesc1=detector.detectAndCompute(trainImg,None)
trainKP2,trainDesc2=detector.detectAndCompute(trainImg,None)
 
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
        image = cv2.cvtColor(curr_img,cv2.COLOR_BGR2GRAY)

        queryKP,queryDesc=detector.detectAndCompute(image,None)
        queryKP1,queryDesc1=detector.detectAndCompute(image,None)
        queryKP2,queryDesc2=detector.detectAndCompute(image,None)
        matches=flann.knnMatch(queryDesc,trainDesc,k=2)
        matches1=flann.knnMatch(queryDesc1,trainDesc1,k=2)
        matches2=flann.knnMatch(queryDesc2,trainDesc2,k=2)
        
        goodMatch=[]
        for m,n in matches:
            if(m.distance<0.75*n.distance):
                goodMatch.append(m)
        if(len(goodMatch)>MIN_MATCH_COUNT):
            tp=[]
            qp=[]
            for m in goodMatch:
                tp.append(trainKP1[m.trainIdx].pt)
                qp.append(queryKP1[m.queryIdx].pt)
            
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
            
            
        goodMatch1=[]
        for m1,n1 in matches:
            if(m1.distance<0.75*n1.distance):
                goodMatch1.append(m)
        if(len(goodMatch1)>MIN_MATCH_COUNT):
            tp=[]
            qp=[]
            for m in goodMatch1:
                tp.append(trainKP1[m.trainIdx].pt)
                qp.append(queryKP1[m.queryIdx].pt)
            
            tp,qp=np.float32((tp,qp))
            H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
            h,w=trainImg.shape
            trainBorder1=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
            queryBorder1=cv2.perspectiveTransform(trainBorder1,H)
            cv2.polylines(image,[np.int32(queryBorder1)],True,(0,255,0),5)
            print("Image Detected")
            cv2.imshow('result1',image)
        else:
            print ("Not Enough match found- {}/{}".format(len(goodMatch1),MIN_MATCH_COUNT))
            cv2.imshow('result1',image)
            
        goodMatch2=[]
        for m2,n2 in matches:
            if(m2.distance<0.75*n2.distance):
                goodMatch2.append(m2)
        if(len(goodMatch2)>MIN_MATCH_COUNT):
            tp=[]
            qp=[]
            for m2 in goodMatch2:
                tp.append(trainKP2[m.trainIdx].pt)
                qp.append(queryKP2[m.queryIdx].pt)
            
            tp,qp=np.float32((tp,qp))
            H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
            h,w=trainImg.shape
            trainBorder2=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
            queryBorder2=cv2.perspectiveTransform(trainBorder2,H)
            cv2.polylines(image,[np.int32(queryBorder)],True,(0,255,0),5)
            print("Image Detected")
            cv2.imshow('result2',image)
        else:
            print ("Not Enough match found- {}/{}".format(len(goodMatch),MIN_MATCH_COUNT))
            cv2.imshow('result2',image)
        
        #cv2.imshow('thresh',thresh2)
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            break

