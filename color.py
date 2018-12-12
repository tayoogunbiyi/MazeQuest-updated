import RPi.GPIO as GPIO
import time

S0 = 31
S1 = 29
S2 = 3 
S3 = 5
signal = 12
NUM_CYCLES = 10
#GPIO.setmode(GPIO.BOARD)

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
    setup()
    GPIO.output(40,GPIO.LOW)
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
    print("Max is ",max(red,green,blue))
    
    if green<1500 and blue<2000 and red>195 and green > 500 and blue > 500:
        return "red"
        
    elif blue == max(green,blue,red) and blue>3000:
        return "green"
        
    elif blue > green and blue > red and blue>600:
        return "blue"
        
    elif red<250 and green < 500  and blue < 500:
        return "black"
    else:
        return None
    
