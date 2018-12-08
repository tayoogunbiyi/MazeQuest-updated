import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8,GPIO.OUT)
pwm = GPIO.PWM(8, 50)
CURRENT_DC = 7.5
pwm.start(CURRENT_DC)


GPIO.cleanup()
