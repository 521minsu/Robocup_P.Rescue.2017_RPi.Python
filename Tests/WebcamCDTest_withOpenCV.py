import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
cap.set(15,1)

while True:
    ret,image = cap.read()
    Gimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
    Min_GH,Min_GS,Min_GV = 57,59,111
    Max_GH,Max_GS,Max_GV = 89,255,255
          
    #Please Run Calibration.py first, and bring back the values according to the current situation
    Glower = np.array([Min_GH,Min_GS,Min_GV],dtype="uint8")
    Gupper = np.array([Max_GH,Max_GS,Max_GV],dtype="uint8")
    
    Gmask = cv2.inRange(Gimage,Glower,Gupper)
    Gimage, GRcontours,GRhierarchy = cv2.findContours(Gmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    visionmask=cv2.imread('mask_noside.png',0)
    Gres = cv2.bitwise_and(Gmask,Gmask,mask=visionmask)
    Gres, Gcontours,Ghierarchy = cv2.findContours(Gres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
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
    # gx,gy = int(M['m10']/M['m00']), int(M['m01']/M['m00']) - Equation to get center of the mask/contour
    gx,gy = int(M['r10']/M['r00']), int(M['m01']/M['m00'])
    cv2.circle(image,(gx,gy),5,(255,0,0),-1)
          
          
    cv2.imshow('frame',image)
    
    k = cv2.waitKey(1) & 0xFF
    
    if k == 27:
        break
    
cv2.destoryAllWindows()