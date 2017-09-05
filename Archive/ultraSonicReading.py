############################################
#  Robocup_Junior_2017_Premier_UltraSonic  #
# ---------------------------------------- # 
#  Description: This program detects       #
#  obstacles infront of the robot using    #
#  the UltraSonic sensor(HC-SR04)          #
# ---------------------------------------- #
#  Author: Minsu Kim                       #
#  Email : 521minsu@gmail.com              #
#  Last Update: 08.08.17                   #
############################################

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

trig = 15
echo = 13

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
class ultraSonic():
  def value():
    GPIO.output(trig, False)
    time.sleep(0.1)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    while GPIO.input(echo) == 0 :
      st = time.time()
    while GPIO.input(echo) == 1 :
      ft = time.time()
    duration = ft - st
    distance = duration * 17000
    distance = round(distance, 2)
        
    return distance