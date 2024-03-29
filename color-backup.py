import RPi.GPIO as GPIO
import time

S0 = 31
S1 = 29
S2 = 3 
S3 = 5
signal = 12
NUM_CYCLES = 10
GPIO.setmode(GPIO.BOARD)

def setup():
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(S1,GPIO.OUT)
  GPIO.setup(S0,GPIO.OUT)
  GPIO.setup(S2,GPIO.OUT)
  GPIO.setup(S3,GPIO.OUT)
  GPIO.output(S1,GPIO.HIGH)
  GPIO.output(S0,GPIO.HIGH)
  GPIO.setup(40,GPIO.OUT)
  print("\n")
  


GPIO.setwarnings(False)

def get_color():
    GPIO.output(40,GPIO.HIGH)
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   

    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration


    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration

    print(red)
    print(green)
    print(blue)
    if green<1500 and blue<2000 and red>195:
        return "red"
        
    elif green > red and  green > blue and green>600:
        return "green"
        
    elif blue > green and blue > red and blue>600:
        return "blue"
        
    elif red<200 and green < 250  and blue < 250:
        return "black"
    else:
        return None
    

