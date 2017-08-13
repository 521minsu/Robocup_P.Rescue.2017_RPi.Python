import serial, time, struct

ser = serial.Serial('/dev/ttyUSB0',9600)

def value(sensor):
    while ser.inWaiting()==0:
        pass
    try:
        rawData  = ser.readline().strip()
        if rawData != b'':
            rawrData = rawData.decode()
            senVal = rawrData.split(",")
            proxVal = int(senVal[0])
            irVal = int(senVal[1])
            
            if irVal > 80:
                irVal = 80
            
            if sensor == 'distance':
                return irVal
            elif sensor == 'proximity':
                return proxVal
            
##            print("Raw:{} \t Prox: {} \t Distance:{}".format(rawData,proxVal,irVal))
##            print(rawData)
##        sensorValue = int(rawrData)
##        rawrData = struct.unpack("", rawData)
##        sensorValue = (rawrData[0] << 8) | rawrData[1]
##            time.sleep(0.2)
        else:
            pass
    except:
        print("Passed an error")
        pass
    