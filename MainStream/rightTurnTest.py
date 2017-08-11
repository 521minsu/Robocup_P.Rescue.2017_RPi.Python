import dc_motors as abc
import time
dc = abc.Motor.drivingcontrol

for i in range(0,10):
    dc(dc,0,0)
    dc(dc,-100,100)
    time.sleep(0.78)
    dc(dc,0,0)
    time.sleep(2)