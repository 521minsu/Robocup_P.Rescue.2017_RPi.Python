import serial, time, struct

ser = serial.Serial('/dev/ttyUSB1',9600)

while True:
    while ser.inWaiting()==0:
        pass
##    rawData = ser.readline()
##    print(rawData)
    try:
        rawData  = ser.readline().strip()
        if rawData != b'':
            rawrData = int(rawData)
            print("Sensor value: {}".format(rawrData))
        #sensorValue = int(rawrData)
    #    rawrData = struct.unpack("", rawData)
    #    sensorValue = (rawrData[0] << 8) | rawrData[1]
        
            #time.sleep(0.2)
        else:
            pass
    except:
        print("Passed an error")
        pass
    