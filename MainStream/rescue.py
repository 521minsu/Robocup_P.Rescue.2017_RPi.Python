########################################
#  Robocup_Junior_2017_Premier_Rescue  #
# ------------------------------------ # 
#  Description: This program controls  #
#  and directs the robot when it       #
#  has reached the rescue tile.        #
# ------------------------------------ #
#  Author: Minsu Kim                   #
#  Email : 521minsu@gmail.com          #
#  Last Update: 20.08.17               #
########################################

#Camera & Opencv related modules
import time

# motor related module
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol

import SensorReading as SR
    
#####################################################################
def catchVictim():
    dist = SR.value('distance')
    # Catches the victim after finding it
    while dist > 10:
        dc(dc,100,100)
        dist = SR.value('distance')
    # Travels forward for 0.5 more seconds to make sure it is possible to catch the victim
    dc(dc,100,100)
    time.sleep(0.5)
    # Controls the lifting mechanism in order to catch and lift the victim up
    dc(dc,0,0)
    lc(lc,'idle','catch')
    time.sleep(0.5)
    lc(lc,'lift','catch')
    time.sleep(0.5)
    # Calls the searchPlatform function and searches for the platform
    searchPlatform()


def searchPlatform():
    dist = SR.value('distance')
    startTime = round(time.time())
    searchDir = 0
    
    while dist > 25:
        dist = SR.value('distance')
        
        curTime = round(time.time())
        TimePassed = curTime - startTime
        
        if TimePassed >= 2:
            if searchDir == 0:
                searchDir = 1
            elif searchDir == 1:
                searchDir = 0
            startTime = round(time.time())
        
        if searchDir == 0:
            dc(dc,-75,75)
        elif searchDir == 1:
            dc(dc,75,-75)
    
    dc(dc,0,0)
    print("Platform Found... Entering the Final Phrase...")
    placeAndFinish()
    
def placeAndFinish():
    dist = SR.value('distance')
    # Go straight until IR sensor returns 8cm or less
    while dist > 8:
        dc(dc,100,100)
    # Go straight for 0.5 seconds more in order to make sure that there is a platform in front of the robot
    dc(dc,100,100)
    time.sleep(0.5)
    # Stop to release/place the victim
    dc(dc,0,0)
    
    lc(lc,'idle','release')
    
    dc(dc,-100,-100)
    time.sleep(2)
    dc(dc,0,0)
    finished = True
    finish()
    
    
def finish():
    if finished == True:
        dc_motors.Motor.cleanup()