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
