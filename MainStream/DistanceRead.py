import SensorReading as SR

while True:
    dist = SR.value('distance')
    print("There is an obstacle {}cm infront of the robot".format(dist))