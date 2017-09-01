########################################
#  Robocup_Junior_2017_Premier_Rescue  #
# ------------------------------------ # 
#  Description: This program controls  #
#  and directs the robot when it       #
#  has reached the rescue tile.        #
# ------------------------------------ #
#  Author: Minsu Kim                   #
#  Email : 521minsu@gmail.com          #
#  Last Update: 22.08.17               #
########################################

import time

# motor related module
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol

import SensorReading as SR
    
#####################################################################
def searchVictim(searchDir):
    edgeReached = 0
    prev_detection = 'other'
    
    while edgeReached < 2:
        if searchDir == 0:
            dc(dc,75,-75)
        elif searchDir == 1:
            dc(dc,-75,75)
        
        for i in range(5):
            lCSVal = SR.value('left_CS')
            rCSVal = SR.value('right_CS')
            
        if edgeReached == 0 and lCSVal == 'other':
            dc(dc,0,0)
            startTime = time.time()
            prev_detection = 'left'
            searchDir = 0
        elif edgeReached == 0 and rCSVal == 'other':
            dc(dc,0,0)
            startTime = time.time()
            prev_detection = 'right'
            searchDir = 1
            
        if edgeReached == 1 and lCSVal == 'other' and prev_detection == 'right':
            dc(dc,0,0)
            curTime = time.time()
            turnTime = curTime - startTime
            searchDir = 1
            edgeReached = 2
        elif edgeReached == 1 and rCSVal == 'other' and prev_detection == 'left':
            dc(dc,0,0)
            curTime = time.time()
            turnTime = curTime - startTime
            searchDir = 0
            edgeReached = 2
            
            
            
    numberofArrays = 40
    arrayTime = turnTime/numberofArrays
    arrayTime = arrayTime/1000
    
    arrayDistance = []
    
    for i in range(0,numberofArrays):
        if searchDir == 0:
            dc(dc,75,-75)
        if searchDir == 1:
            dc(dc,-75,75)
        time.sleep(arrayTime)
        for i in range(5):
            dist = SR.value('distance')
        arrayDistance.append(dist)
        print("Detecting in progress... i:{} \t dist:{}".format(i,dist))
    if searchDir == 0:
        searchDir = 1
    elif searchDir == 1:
        searchDir = 0
    dc(dc,0,0)
    raise "TypeError"
          

def catchVictim():
    dist = 80 # Minimise the number of SR call
    # Catches the victim after finding it
    while dist > 9:
        dc(dc,100,100)
        dist = SR.value('distance')
        print("Approaching Victim... dist:{}".format(dist))
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
    dist = 80
    searchPlatform(dist)


def searchPlatform(distance):
    dist = distance
    startTime = round(time.time())
    searchDir = 0
    
    while dist > 25:
        dist = SR.value('distance')
        print("Searching for the platfrom... dist:{}".format(dist))
        
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
    dist = 80
    placeAndFinish(dist)
    
def placeAndFinish(distance):
    dist = distance
    # Go straight until IR sensor returns 8cm or less
    while dist > 8:
        dist = SR.value('distance')
        dc(dc,100,100)
        print("Approaching the platfrom... dist:{}".format(dist))
        
    # Go straight for 0.5 seconds more in order to make sure that there is a platform in front of the robot
    dc(dc,100,100)
    time.sleep(0.5)
    # Stop to release/place the victim
    dc(dc,0,0)
    
    lc(lc,'idle','release')
    time.sleep(1)
    
    dc(dc,-100,-100)
    time.sleep(0.75)
    dc(dc,0,0)
    finished = True
    finish()
    
    
def finish():
    print("Finished the rescue sequence...")
    dc_motors.Motor.cleanup(dc_motors)