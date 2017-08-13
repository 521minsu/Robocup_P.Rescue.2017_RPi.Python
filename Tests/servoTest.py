import RPi.GPIO as IO
import time

IO.setmode(IO.BOARD)
IO.setup(22,IO.OUT)

pwm=IO.PWM(22,50)

pwm.start(1)
time.sleep(0.5)
pwm.stop()