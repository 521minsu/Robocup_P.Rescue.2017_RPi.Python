import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

def Test(PiPin):
    measurement = 0
    GPIO.setup(PiPin,GPIO.OUT)
    GPIO.output(PiPin,GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(PiPin,GPIO.IN)
    
    while (GPIO.input(PiPin) == GPIO.LOW):
        measurement += 1
    
    return measurement

while True:
    val = Test(36)
    print("Result:{}".format(val))
    
