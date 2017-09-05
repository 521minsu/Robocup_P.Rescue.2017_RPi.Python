import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
cap.set(15,1)

while True:
    ret,frame = cap.read()
    
    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5) & 0xFF
    
    if k == 27:
        break
    
cv2.destoryAllWindows()