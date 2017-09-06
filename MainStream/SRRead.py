import SensorReading as SR
import dc_motors
dc = dc_motors.Motor.drivingcontrol

while True:
##    lCSVal = SR.value('left_CS_Raw')
##    rCSVal = SR.value('right_CS_Raw')
##    lCSColor = SR.value('left_CS')
##    rCSColor = SR.value('right_CS')
##    print("Left: Color:{}  Raw:{} \t Right: Color:{}  Raw:{}".format(lCSColor,lCSVal,rCSColor,rCSVal))
    dist = SR.value('distance')
    print("In rescue... dist:{}".format(dist))
    #dc(dc,-75,75)
    dc(dc,0,0)
