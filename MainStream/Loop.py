######################################
#  Robocup_Junior_2017_Premier_Loop  #
# ---------------------------------- # 
#  Description: This program decides #
#  on the movement of the robot and  #
#  calls the required modules        #
# ---------------------------------- #
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 08.08.17             #
######################################

import time
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
import waterTowers as WT



def __init__():
    pass

class MainControl(object):
    def linetrace(self,error):
        mSpeed = 100
        Kp,Ki,Kd = 100,10,0    # 100,10,0
        integral,derivative,lasterror = 0,0,0
        pidturn = 0
        if error != 9000:
            integral += error
            derivative = error - lasterror
            pidturn = Kp*error + Ki*integral + Kd*derivative
            pidturn = pidturn/100
            lasterror = error
            Lspeed,Rspeed = mSpeed-pidturn, mSpeed+pidturn
            if Lspeed > 100:
                Lspeed = 100
            elif Lspeed < -100:
                Lspeed = -100
            if Rspeed > 100:
                Rspeed = 100
            elif Rspeed < -100:
                Rspeed = -100
            print("Left:{} \t Right:{} \t error:{} \t lasterror:{} \t integral:{} \t derivative:{} \t pidturn:{}".format(Lspeed,Rspeed,error,lasterror,integral,derivative,pidturn))
            dc(dc,Lspeed,Rspeed)
        else:
            pass
    
    def greenturn(self,turnerror):
        # 100 - 110
        if turnerror < 0: # turn left
            dc(dc,0,0)
            dc(dc,100,100)
            time.sleep(0.9)
            dc(dc,0,0)
            dc(dc,100,-100)
            time.sleep(0.85)
            dc(dc,0,0)
            dc(dc,-100,100)
            print("turned left")
        elif turnerror > 0: # turn right
            dc(dc,0,0)
            dc(dc,100,100)
            time.sleep(0.9)
            dc(dc,0,0)
            dc(dc,-100,100)
            time.sleep(0.85)
            dc(dc,0,0)
            dc(dc,100,-100)
            print("turned right")
        else:
            pass # Maybe an error has occured during the run, ignoring the call... 
    def watertower(self,usval):
        if usval < 30:   # When there is an obstacle in 30cm range...
            dc(dc,0,0)
            WT.watertower()
    
    def rescuedetection(self,rx,ry):
        pass # add link to rescue program and program it there