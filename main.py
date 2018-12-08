import threading

import RPi.GPIO as GPIO
from time import sleep
from servo import set_neutral,turn_left,turn_right,adjust_left,adjust_right
from ultrasonic import check_right_left,read_distance

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8,GPIO.OUT)
pwm = GPIO.PWM(8, 50)
CURRENT_DC = 7.5
pwm.start(CURRENT_DC)

set_neutral(pwm)

FRONT_TRIG = 37
FRONT_ECHO = 38

RIGHT_TRIG = 33
RIGHT_ECHO = 35

LEFT_TRIG = 19
LEFT_ECHO = 21


GPIO.setup(LEFT_TRIG,GPIO.OUT)
GPIO.output(LEFT_TRIG,0)
GPIO.setup(LEFT_ECHO,GPIO.IN)

GPIO.setup(RIGHT_TRIG,GPIO.OUT)
GPIO.output(RIGHT_TRIG,0)
GPIO.setup(RIGHT_ECHO,GPIO.IN)

GPIO.setup(FRONT_TRIG,GPIO.OUT)
GPIO.output(FRONT_TRIG,0)
GPIO.setup(FRONT_ECHO,GPIO.IN)

#Left
Motor1E = 11
Motor1B = 15
Motor1A = 13
 
Motor2B = 7
Motor2A = 18
Motor2E = 16
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
 
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
 
def forward():
    print "Going forwards"
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
 
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
 
def backward(): 
    print "Going backwards"
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
 
def stop():
    print "Now stop"
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)



def spin():
    set_neutral
    sleep(0.5)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    sleep(0.2)
def front_distance():
    print("Calling front distance")
    i = 0 
    i+=1
    distance = read_distance(FRONT_ECHO,FRONT_TRIG)
    print("distance : ",distance)
    if distance < 10:
        print("Distance is less than 10")
        stop()
        sleep(0.1)
        backward()
        sleep(0.5)
        spin()
        sleep(0.75)
        stop()
        sleep(0.1)
        forward()
    else:
        pass



# left_right_thread = threading.Thread(target=check_right_left,args=(
#     LEFT_ECHO,
#     RIGHT_ECHO,
#     LEFT_TRIG,
#     RIGHT_TRIG,
#     pwm,))

def adjust(adjust_left,adjust_right,FAVORED_SIDE,CURRENT_DC):
    if FAVORED_SIDE == 'right':
        print("Calling adj right")
        CURRENT_DC = adjust_right(pwm,CURRENT_DC)
        sleep(0.2)
        set_neutral(pwm)
        sleep(0.2)
    else:
        print("Calling adj left")
        CURRENT_DC = adjust_left(pwm,CURRENT_DC)
        sleep(0.2)
        set_neutral(pwm)
        sleep(0.2)
    return


FAVORED_SIDE = None

try:
    while True:
                
        adjust_thread = threading.Thread(target=adjust,args=(adjust_left,adjust_right,FAVORED_SIDE,CURRENT_DC))
        data = check_right_left(LEFT_ECHO,RIGHT_ECHO,LEFT_TRIG,RIGHT_TRIG,pwm)
        if(data[0] < 7 or data[1] < 7):
            if(data[0] < 7):
                FAVORED_SIDE = "right"
                adjust_thread.start()
            else:
                FAVORED_SIDE =  "left"
                adjust_thread.start()
        else:
            continue

except:
    GPIO.cleanup()


# GPIO.cleanup()
