import RPi.GPIO as GPIO
import time

def read_distance(ECHO,TRIG):
    GPIO.output(TRIG,1)
    time.sleep(0.000001)
    GPIO.output(TRIG,0)


    while GPIO.input(ECHO) == 0:
        pass
    
    start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pass
    
    stop = time.time()

    return (stop-start) * 17000

def check_right_left(ECHO1,ECHO2,TRIG1,TRIG2):
    '''
    ECHO1 & TRIG1 - Echo and trig pins of left sensor
    ECHO2 & TRIG2- Echo and trig pins of the right sensor
    '''
    dist1 = read_distance(ECHO1,TRIG1)
    dist2 = read_distance(ECHO2,TRIG2)

    diff = dist1 - dist2
    if abs(diff): 
        pass

