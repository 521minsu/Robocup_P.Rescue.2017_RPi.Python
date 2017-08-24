######################################
#  Robocup_Junior_2017_Premier_SR    #
# ---------------------------------- # 
#  Description: This program relays  #
#  sensor datas from Arduino Nano to #
#  Python using Pyserial and serial  #
#  print option on Arduino           #
# ---------------------------------- #
#  Author: Minsu Kim                 #
#  Email : 521minsu@gmail.com        #
#  Last Update: 23.08.17             #
######################################

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
    
###########################
# Debugging Purpose Only! #
###########################
##if __name__ == "__main__":
##    while True:
##        while ser.inWaiting()==0:
##            pass
##        rawData  = ser.readline().strip()
##        if rawData != b'':
##            rawrData = rawData.decode()
##            senVal = rawrData.split(",")
##            proxVal = int(senVal[0])
##            irVal = int(senVal[1])
##            
##            if irVal > 80:
##                irVal = 80
##        print(rawData)
        #print("Raw:{} \t Dist:{} \t Prox:{}".format(rawData,irVal,senVal))
