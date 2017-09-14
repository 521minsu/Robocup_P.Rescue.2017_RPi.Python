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

ser = serial.Serial('/dev/ttyACM0',9600)

def value(sensor):
    while ser.in_waiting()==0:
        pass
    try:
        rawData  = ser.readline().strip()
        if rawData != b'':
            rawrData = rawData.decode()
            senVal = rawrData.split(",")
            dist = int(senVal[0])
                
            if sensor == 'distance':
                return dist
    except:
        print("Passed an error")
        pass

def write(val):
    try:
        send = val
        ser.write(send.encode())
    except:
        print("Passed an error while sending val to arduino...")
        pass