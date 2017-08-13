########################################
#  Robocup_Junior_2017_Premier_Servo   #
# ------------------------------------ #
#  Description: This program is in     #
#  charge of controlling servo motors  #
#  based on the calls from other files #
# ------------------------------------ # 
#  Author: Minsu Kim                   #
#  Email : 521minsu@gmail.com          #
#  Last Update: 28.07.17               #
########################################
import RPi.GPIO as GPIO
import time

servoPin = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin,GPIO.OUT)

servopwm = GPIO.PWM(servoPin,50)

servopwm.start(1)
time.sleep(0.5)
servopwm.ChangeDutyCycle(5)
time.sleep(0.5)
        
servopwm.stop()

        
class control():
    def up():
        servopwm.start(12)
        time.sleep(0.5)
        
        servopwm.stop()

    def down():
        servopwm.start(12)
        time.sleep(0.5)
        
        servopwm.stop()
