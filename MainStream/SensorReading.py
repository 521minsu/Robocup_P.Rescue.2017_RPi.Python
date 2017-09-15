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
#  Last Update: 15.09.17             #
######################################

import serial, time, struct

ser = serial.Serial('/dev/ttyACM0',9600)

def write(val):
    try:
        send = val
        ser.write(send.encode())
    except:
        print("Passed an error while sending val to arduino...")
        pass