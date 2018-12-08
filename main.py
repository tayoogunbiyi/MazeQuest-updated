import RPi.GPIO as GPIO
from time import sleep
from servo import set_neutral,turn_left,turn_right,adjust_left,read_distance
 
GPIO.setmode(GPIO.BOARD)

GPIO.setup(8,GPIO.OUT)
pwm = GPIO.PWM(8, 50)
CURRENT_DC = 7.5
pwm.start(CURRENT_DC)

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
    #Turn servo to full angle
    adjust_left(pwm)
    sleep(0.5)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    sleep(0.2)
    set_neutral(pwm)



spin()
sleep(0.5)
GPIO.cleanup()