def go(Lspeed,Rspeed,zzz):
    import dc_motors,time
    dc = dc_motors.Motor.drivingcontrol

    dc(dc,Lspeed,Rspeed)
    time.sleep(zzz)
    dc_motors.Motor.cleanup(dc_motors)