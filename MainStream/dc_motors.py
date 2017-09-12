########################################
#  Robocup_Junior_2017_Premier_Motor   #
# ------------------------------------ #
#  Description: This program is in     #
#  charge of controlling dc motors     #
#  based on the calls from other files #
# ------------------------------------ #
#  Author: Minsu Kim                   #
#  Email : 521minsu@gmail.com          #
#  Last Update: 24.07.17               #
########################################

import RPi.GPIO as GPIO
import time

# GPIO MODE IS SET TO GPIO PIN NUMBER
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

right_pwm_pin = 32 
right_in1_pin = 11
right_in2_pin = 7
left_pwm_pin = 33
left_in1_pin = 16
left_in2_pin = 18

lift_pwm_pin = 38
lift_in1_pin = 37
lift_in2_pin = 40
catch_pwm_pin = 29
catch_in1_pin = 24
catch_in2_pin = 26

camera_pwm_pin = 19
camera_in1_pin = 21
camera_in2_pin = 23


GPIO.setup(left_in1_pin, GPIO.OUT)
GPIO.setup(left_in2_pin, GPIO.OUT)
GPIO.setup(left_pwm_pin, GPIO.OUT)
GPIO.setup(right_in1_pin, GPIO.OUT)
GPIO.setup(right_in2_pin, GPIO.OUT)
GPIO.setup(right_pwm_pin, GPIO.OUT)

GPIO.setup(lift_in1_pin, GPIO.OUT)
GPIO.setup(lift_in2_pin, GPIO.OUT)
GPIO.setup(lift_pwm_pin, GPIO.OUT)
GPIO.setup(catch_in1_pin, GPIO.OUT)
GPIO.setup(catch_in2_pin, GPIO.OUT)
GPIO.setup(catch_pwm_pin, GPIO.OUT)

GPIO.setup(camera_pwm_pin, GPIO.OUT)
GPIO.setup(camera_in1_pin, GPIO.OUT)
GPIO.setup(camera_in2_pin, GPIO.OUT)

left_dmotor_p = GPIO.PWM(left_pwm_pin, 255)
right_dmotor_p = GPIO.PWM(right_pwm_pin, 255)
left_dmotor_p.start(0)
right_dmotor_p.start(0)

def __init__ ():
    pass

class Motor(object):
    def drivingcontrol(self, lms, rms):        
        if lms > 0:
            GPIO.output(left_in1_pin, False)
            GPIO.output(left_in2_pin, True)
            left_dmotor_p.ChangeDutyCycle(lms)
        elif lms < 0:
            GPIO.output(left_in1_pin, True)
            GPIO.output(left_in2_pin, False)
            left_dmotor_p.ChangeDutyCycle(abs(lms))
        elif lms == 0:
            GPIO.output(left_in1_pin, False)
            GPIO.output(left_in2_pin, False)
            left_dmotor_p.ChangeDutyCycle(0)
        if rms > 0:
            GPIO.output(right_in1_pin, False)
            GPIO.output(right_in2_pin, True)
            right_dmotor_p.ChangeDutyCycle(rms)
        elif rms < 0:
            GPIO.output(right_in1_pin, True)
            GPIO.output(right_in2_pin, False)
            right_dmotor_p.ChangeDutyCycle(abs(rms))
        elif rms == 0:
            GPIO.output(right_in1_pin, False)
            GPIO.output(right_in2_pin, False)
            right_dmotor_p.ChangeDutyCycle(0)
            
    
    def liftcontrol(self, lift, catch):
        if lift == 'lift':
            GPIO.output(lift_in1_pin, True)
            GPIO.output(lift_in2_pin, False)
            GPIO.output(lift_pwm_pin, True)
        elif lift == 'release':
            GPIO.output(lift_in1_pin, False)
            GPIO.output(lift_in2_pin, True)
            GPIO.output(lift_pwm_pin, True)
            time.sleep(1.5)
            GPIO.output(lift_in1_pin, False)
            GPIO.output(lift_in2_pin, False)
            GPIO.output(lift_pwm_pin, False)
        elif lift == 'idle':
            GPIO.output(lift_in1_pin, False)
            GPIO.output(lift_in2_pin, False)
            GPIO.output(lift_pwm_pin, False)
            
        if catch == 'release':
            GPIO.output(catch_in1_pin, True)
            GPIO.output(catch_in2_pin, False)
            GPIO.output(catch_pwm_pin, True)
            time.sleep(0.5)
            GPIO.output(catch_in1_pin, False)
            GPIO.output(catch_in2_pin, False)
            GPIO.output(catch_pwm_pin, False)
        elif catch == 'catch':
            GPIO.output(catch_in1_pin, False)
            GPIO.output(catch_in2_pin, True)
            GPIO.output(catch_pwm_pin, True)
            
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
        right_dmotor_p.stop()
        GPIO.output(right_in1_pin, False)
        GPIO.output(right_in2_pin, False)
        left_dmotor_p.stop()
        GPIO.output(left_in1_pin, False)
        GPIO.output(left_in2_pin, False)
        GPIO.cleanup()

