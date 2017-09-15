########################################
#  Robocup_Junior_2017_Premier_Motor   #
# ------------------------------------ #
#  Description: This program is in     #
#  charge of controlling dc motors     #
#  based on the calls from other files #
# ------------------------------------ #
#  Author: Minsu Kim                   #
#  Email : 521minsu@gmail.com          #
#  Last Update: 15.09.17               #
########################################

import RPi.GPIO as GPIO
import time

# GPIO MODE IS SET TO GPIO PIN NUMBER
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

camera_pwm_pin = 19
camera_in1_pin = 21
camera_in2_pin = 23

GPIO.setup(camera_pwm_pin, GPIO.OUT)
GPIO.setup(camera_in1_pin, GPIO.OUT)
GPIO.setup(camera_in2_pin, GPIO.OUT)

def __init__ ():
    pass

class Motor(object):  
    def cameracontrol(self,tilt):
        if tilt == 'up':
            GPIO.output(camera_in1_pin, True)
            GPIO.output(camera_in2_pin, False)
            GPIO.output(camera_pwm_pin, True)
        elif tilt == 'down':
            GPIO.output(camera_in1_pin, False)
            GPIO.output(camera_in2_pin, True)
            GPIO.output(camera_pwm_pin, True)
        elif tilt == 'stop':
            GPIO.output(camera_in1_pin, False)
            GPIO.output(camera_in2_pin, False)
            GPIO.output(camera_pwm_pin, False)
    
    
    def cleanup(self):
        GPIO.output(camera_in1_pin, False)
        GPIO.output(camera_in2_pin, False)
        GPIO.output(camera_pwm_pin, False)
        GPIO.cleanup()

