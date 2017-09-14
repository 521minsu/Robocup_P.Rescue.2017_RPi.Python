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
    def linetrace(self,error,Kp,Ki,Kd,startTime):
        mSpeed = 100
        integral,derivative,lasterror = 0,0,0
        pidturn = 0
        if error != 1000:
            integral += error
            derivative = error - lasterror
            pidturn = Kp*error + Ki*integral + Kd*derivative
            pidturn = pidturn/100
            lasterror = error
            
            Lspeed,Rspeed = mSpeed+pidturn, mSpeed-pidturn
##            if 35 > Lspeed >= 0:
##                Lspeed = -10
##                print("(POS) Lspeed calibrated to.... {}".format(Lspeed))
##            elif 0 > Lspeed > -35:
##                Lspeed -= 10
##                print("(NEG) Lspeed calibrated to.... {}".format(Lspeed))
##            if 35 > Rspeed >= 0:
##                Rspeed = -10
##                print("(POS) Rspeed calibrated to.... {}".format(Rspeed))
##            elif 0 > Rspeed > -35:
##                Rspeed -= 10
##                print("(NEG) Rspeed calibrated to.... {}".format(Rspeed))
            if Lspeed > 90:
                Lspeed = 90
            elif Lspeed < -90:
                Lspeed = -90
            if Rspeed > 90:
                Rspeed = 90
            elif Rspeed < -90:
                Rspeed = -90
            curTime = round(time.time())
            timePassed = curTime - startTime
            print("ERROR:{} \t pidturn:{} timestamp:{} \t Lspeed:{} \t Rspeed:{}".format(error,pidturn,curTime,Lspeed,Rspeed))
            dc(dc,Lspeed,Rspeed)
        else:
            pass
        
    def noblack():
        array = SR.value('IRArray')
        Lspeed,Rspeed = 0,0
        if array == 2:
            Lspeed,Rspeed = -100,100
        elif array == 4:
            Lspeed,Rspeed = -90,100
        elif array == 8:
            Lspeed,Rspeed = 100,100
        elif array == 16:
            Lspeed,Rspeed = 100,-90
        elif array == 32:
            Lspeed,Rspeed = 100,-100
        elif array == 6:
            Lspeed,Rspeed = -90,100
        elif array == 14:
            Lspeed,Rspeed = -100,100
        elif array == 12:
            Lspeed,Rspeed = -90,100
        elif array == 28:
            Lspeed,Rspeed = 100,100
        elif array == 24:
            Lspeed,Rspeed = 100,-90
        elif array == 56:
            Lspeed,Rspeed = 100,-100
        elif array == 48:
            Lspeed,Rspeed = 100,-90
        elif array == 60:
            Lspeed,Rspeed = 100,-100
        elif array == 30:
            Lspeed,Rspeed = -100,100
        print("There was NO black detected... array:{} \t Lspeed:{} \t Rspeed:{}".format(array,Lspeed,Rspeed))
        dc(dc,Lspeed,Rspeed)
        
    def greenturn(self,turnerror):
        straight = 0.01    #0.65 before
        right = 0.3
        left = 0.4
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
