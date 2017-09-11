######################################
#  Robocup_Junior_2017_Premier_Loop  #
# ---------------------------------- # 
#  Description: This program decides #
#  on the movement of the robot and  #
#  calls the required modules        #
# ---------------------------------- #
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 10.09.17             #
######################################

import time
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
import SensorReading as SR

def __init__():
    pass

class MainControl(object):
    def linetrace(self,error,Kp,Ki,Kd):
        mSpeed = 100
        integral,derivative,lasterror = 0,0,0
        pidturn = 0
        if error != 1000:
##            integral += error
##            derivative = error - lasterror
##            pidturn = Kp*error + Ki*integral + Kd*derivative
##            pidturn = pidturn/100
##            lasterror = error
            if error < 0:
                pidturn = (-200/140**2)*error**2
            elif error > 0:
                pidturn = (200/140**2)*error**2
    
##        if error != 1000:
##            mSpeed = 100
##            pidturn = (10/7)*error
            Lspeed,Rspeed = mSpeed+pidturn, mSpeed-pidturn
            if 35 > Lspeed >= 0:
                Lspeed = -10
                print("(POS) Lspeed calibrated to.... {}".format(Lspeed))
            elif 0 > Lspeed > -35:
                Lspeed -= 10
                print("(NEG) Lspeed calibrated to.... {}".format(Lspeed))
            if 35 > Rspeed >= 0:
                Rspeed = -10
                print("(POS) Rspeed calibrated to.... {}".format(Rspeed))
            elif 0 > Rspeed > -35:
                Rspeed -= 10
                print("(NEG) Rspeed calibrated to.... {}".format(Rspeed))
            if Lspeed > 100:
                Lspeed = 100
            elif Lspeed < -100:
                Lspeed = -100
            if Rspeed > 100:
                Rspeed = 100
            elif Rspeed < -100:
                Rspeed = -100
            print("ERROR:{} \t pidturn:{} Lspeed:{} \t Rspeed:{}".format(error,pidturn,Lspeed,Rspeed))
            dc(dc,Lspeed,Rspeed)
        else:
            pass
    
    def greenturn(self,turnerror):
        straight = 0.8    #0.65 before
        right = 0.9
        left = 1
        if turnerror != 0:
            dc(dc,0,0)
            dc(dc,100,100)
            time.sleep(straight)
            dc(dc,0,0)
        if turnerror > 0: # turn right
            dc(dc,100,-100)
            time.sleep(right)
            dc(dc,0,0)
            dc(dc,-100,100)
            print("turned right")
        elif turnerror < 0: # turn left
            dc(dc,-100,100)
            time.sleep(left)
            dc(dc,0,0)
            dc(dc,100,-100)
            print("turned left")
        else:
            pass # Maybe an error has occured during the run, ignoring the call... 
