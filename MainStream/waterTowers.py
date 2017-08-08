############################################
#  Robocup_Junior_2017_Premier_WaterTowers #
# ---------------------------------------- # 
#  Description: This program executes the  #
#  required motion in order to avoid a     #
#  water tower that is located <30cm       #
#  infront of the robot                    #
# ---------------------------------------- #
#  Author: Minsu Kim                       #
#  Email : 521minsu@gmail.com              #
#  Last Update: 08.08.17                   #
############################################

import dc_motors
import time
dc = dc_motors.Motor.drivingcontrol

def watertower():
     dc(dc,100,-100)
     time.sleep(0.5)
     dc(dc,100,100)
     time.sleep(0.2)
     dc(dc,30,100)
     time.sleep(2)
