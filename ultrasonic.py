def read_distance(ECHO):
    GPIO.output(10,1)
    time.sleep(0.000001)
    GPIO.output(10,0)


    while GPIO.input(ECHO) == 0:
        pass
    
    start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pass
    
    stop = time.time()

    return (stop-start) * 17000
