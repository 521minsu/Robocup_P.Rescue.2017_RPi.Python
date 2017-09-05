import SensorReading as SR

while True:
    lCSVal = SR.value('left_CS_Raw')
    rCSVal = SR.value('right_CS_Raw')
    lCSColor = SR.value('left_CS')
    rCSColor = SR.value('right_CS')
    print("Left: Color:{}  Raw:{} \t Right: Color:{}  Raw:{}".format(lCSColor,lCSVal,rCSColor,rCSVal))
