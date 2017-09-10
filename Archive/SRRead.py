import SensorReading as SR

while True:
    prox = SR.value('proximity')
    print("Prox:{}".format(prox))
