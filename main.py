import threading

import RPi.GPIO as GPIO
from time import sleep
from servo import set_neutral,turn_left,turn_right,adjust_left,adjust_right
from ultrasonic import check_right_left,read_distance
from color import get_color

MOVING_BACKWARDS = False

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

NOT_MOVING_COUNT = 0

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
    MOVING_BACKWARDS = False
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
 
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    return False
 
def backward(): 
    print "Going backwards"
    MOVING_BACKWARDS = True
    print("Setting backwards to true :",MOVING_BACKWARDS)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    return True
 
def stop():
    print "Now stop"
    MOVING_BACKWARDS = False
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    return False


def spin(direction='default'):
    '''
    Don't pass anything when turning 180 deg
    '''
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    if direction == 'default':
        interval = 0.80
        balanced = False
        while not balanced:
            data = check_right_left(LEFT_ECHO,RIGHT_ECHO,LEFT_TRIG,RIGHT_TRIG,pwm)
            if not data : continue
            if(data[0] < 7 or data[1] < 7):
                if(data[0] < 7):
                    if MOVING_BACKWARDS:
                        FAVORED_SIDE = "left"
                    else:
                        FAVORED_SIDE = "right"
                    adjust_thread = threading.Thread(target=adjust,args=(adjust_left,adjust_right,FAVORED_SIDE,CURRENT_DC))
                    adjust_thread.start()
                    
                else:
                    if MOVING_BACKWARDS:
                        FAVORED_SIDE = "right"
                    else:
                        FAVORED_SIDE = "left"
                    adjust_thread = threading.Thread(target=adjust,args=(adjust_left,adjust_right,FAVORED_SIDE,CURRENT_DC))
                    adjust_thread.start()
            if(data[0] > 5 or data[1] > 5):
                balanced = True

    elif direction == 'left':
        interval = 0.45
    else:
        interval = 0.40
    
    turn_right(pwm)
    sleep(0.1)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
        
    if direction == 'right':
        
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        sleep(interval)
        set_neutral(pwm)
        MOVING_BACKWARDS = stop()
        return
    else:
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        sleep(interval)
        set_neutral(pwm)
        MOVING_BACKWARDS = stop()
    print("Direction : ",direction)
    print("INterval :",interval)
        

# left_right_thread = threading.Thread(target=check_right_left,args=(
#     LEFT_ECHO,
#     RIGHT_ECHO,
#     LEFT_TRIG,
#     RIGHT_TRIG,
#     pwm,))

def adjust(adjust_left,adjust_right,FAVORED_SIDE,CURRENT_DC):
    print("favored side : ",FAVORED_SIDE)
    if FAVORED_SIDE == 'right':
        print("Calling adj right")
        MOVING_BACKWARDS = backward()
        sleep(0.3)
        MOVING_BACKWARDS = stop()
        CURRENT_DC = adjust_right(pwm,CURRENT_DC)
        sleep(0.2)
        set_neutral(pwm)
        sleep(0.2)
    else:
        print("Calling adj left")
        MOVING_BACKWARDS = backward()
        sleep(0.3)
        MOVING_BACKWARDS = stop()
        CURRENT_DC = adjust_left(pwm,CURRENT_DC)
        sleep(0.2)
        set_neutral(pwm)
        sleep(0.2)
    return FAVORED_SIDE


FAVORED_SIDE = None

try:
    while True:
        
        if read_distance(FRONT_ECHO,FRONT_TRIG) < 14:
            print("Stoping...")
            stop()
            sleep(0.1)
            
            print("Color is ",color)
            data = check_right_left(LEFT_ECHO,RIGHT_ECHO,LEFT_TRIG,RIGHT_TRIG,pwm)
            if not data:
                continue
            if(data[0] > data [1]):
                spin("left")
            elif (data[0] < data[1]):
                spin("right")
        data = check_right_left(LEFT_ECHO,RIGHT_ECHO,LEFT_TRIG,RIGHT_TRIG,pwm)
        if not data:
            continue
        if data[0] > (2*data[1]):
            stop()
            sleep(0.2)
            spin("left")
            forward()

        elif data[0] > (2*data[1]):
            stop()
            sleep(0.2)
            spin("right")
            forward()
            
        
        data = check_right_left(LEFT_ECHO,RIGHT_ECHO,LEFT_TRIG,RIGHT_TRIG,pwm)
        if not data:
            continue
        if(data[0] < 5 or data[1] < 5):
            stop()
            sleep(0.1)
            if(data[0] < 5):
                FAVORED_SIDE = "right"
                adjust_thread = threading.Thread(target=adjust,args=(adjust_left,adjust_right,FAVORED_SIDE,CURRENT_DC))
                adjust_thread.start()
                
            else:
                FAVORED_SIDE =  "left"
                adjust_thread = threading.Thread(target=adjust,args=(adjust_left,adjust_right,FAVORED_SIDE,CURRENT_DC))
                adjust_thread.start()
                
                
        else:
            MOVING_BACKWARDS = forward()
            NOT_MOVING_COUNT+=1
            print("Done moving forward ....")
except Exception as e:
    stop()
    GPIO.cleanup()
    print(e)
    GPIO.cleanup()

