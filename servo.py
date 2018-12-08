import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BOARD)


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


def set_neutral(pwm):
    pwm.ChangeDutyCycle(7.5)
    return 7.5
    
def turn_right(pwm):
    pwm.ChangeDutyCycle(12.5)

def turn_left(pwm):
    pwm.ChangeDutyCycle(2.5)

def adjust_left(pwm,duty_cycle):

    if(duty_cycle != 7.5): return duty_cycle
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(Motor2E,GPIO.HIGH)
    
    new_duty_cycle = duty_cycle-2
    pwm.ChangeDutyCycle(new_duty_cycle)
    return new_duty_cycle

def adjust_right(pwm,duty_cycle):
    if duty_cycle != 7.5: return duty_cycle
    GPIO.output(Motor2E,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    new_duty_cycle = duty_cycle+2
    pwm.ChangeDutyCycle(new_duty_cycle)
    return new_duty_cycle

