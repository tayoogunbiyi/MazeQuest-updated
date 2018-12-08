import RPi.GPIO as GPIO
import time
from time import sleep

def set_neutral(pwm):
    pwm.ChangeDutyCycle(7.5)
    return 7.5
    
def turn_right(pwm):
    pwm.ChangeDutyCycle(12.5)

def turn_left(pwm):
    pwm.ChangeDutyCycle(2.5)

def adjust_left(pwm,duty_cycle):
    if(duty_cycle <= 4 ): return 4
    if(duty_cycle != 7.5): return duty_cycle
    new_duty_cycle = duty_cycle-2
    pwm.ChangeDutyCycle(new_duty_cycle)
    return new_duty_cycle

def adjust_right(pwm,duty_cycle):
    if(duty_cycle != 7.5): return duty_cycle
    if(duty_cycle >= 11): return 11
    new_duty_cycle = duty_cycle+2
    pwm.ChangeDutyCycle(new_duty_cycle)
    return new_duty_cycle

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
