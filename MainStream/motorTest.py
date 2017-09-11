import time
import dc_motors
dc = dc_motors.Motor.drivingcontrol
lc = dc_motors.Motor.liftcontrol
cc = dc_motors.Motor.cameracontrol

# Check these before running
#######################################
motor_ENABLE = True                   #
#######################################

cc(cc,'down')
dc(dc,0,0)
lc(lc,'idle','release')

time.sleep(1)
lc(lc,'idle','catch')
time.sleep(1)
lc(lc,'lift','catch')
dc(dc,100,100)
time.sleep(5)
lc(lc,'idle','catch')
time.sleep(2)
lc(lc,'idle','release')


