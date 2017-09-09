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
import SensorReading as SR
import rescue

battery = 10000

def __init__():
    pass

class MainControl(object):
    def linetrace(self,error):
        if battery == 20000:
            mSpeed = 100
            Kp,Ki,Kd = 90,10,0    # New:90,10,0  # Old:120,10,0 
            integral,derivative,lasterror = 0,0,0
            pidturn = 0
        elif battery == 10000:
            mSpeed = 100    # 20000mAh - 100
            Kp,Ki,Kd = 110,15,3# New: @@,@@,0  # Old:80,2,0 
            integral,derivative,lasterror = 0,0,0
            pidturn = 0
        if error != 1000:
            integral += error
            derivative = error - lasterror
            pidturn = Kp*error + Ki*integral + Kd*derivative
            pidturn = pidturn/100
            print(pidturn)
            lasterror = error
            Lspeed,Rspeed = mSpeed+pidturn, mSpeed-pidturn
            if Lspeed > 100:
                Lspeed = 100
            elif Lspeed < -100:
                Lspeed = -100
            if Rspeed > 100:
                Rspeed = 100
            elif Rspeed < -100:
                Rspeed = -100
            #dist = SR.value('distance')
            #print("Left:{} \t Right:{} \t error:{} \t lasterror:{} \t integral:{} \t derivative:{} \t pidturn:{} ".format(Lspeed,Rspeed,error,lasterror,integral,derivative,pidturn,))
            dc(dc,Lspeed,Rspeed)
        else:
            pass
    
    def greenturn(self,turnerror):
        if battery == 20000:
            straight = 0.65
            right = 1
            left = 0.95
        elif battery == 10000:
            straight = 0.65
            right = 0.9
            left = 1
        if turnerror != 0:
            dc(dc,0,0)
            dc(dc,100,100)
            time.sleep(straight)
            dc(dc,0,0)
        if turnerror > 0: # turn right
            dc(dc,100,-100)
            time.sleep(right)    #0.88 - 20000mAh
            dc(dc,0,0)
            dc(dc,-100,100)
            print("turned right")
        elif turnerror < 0: # turn left
            dc(dc,-100,100)
            time.sleep(left)    # 1 - 20000mAh
            dc(dc,0,0)
            dc(dc,100,-100)
            print("turned left")
        else:
            pass # Maybe an error has occured during the run, ignoring the call... 
