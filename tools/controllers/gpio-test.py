from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM) # Choose BCM to use GPIO numbers instead of pin numbers
GPIO.setup(17, GPIO.OUT)
time.sleep(1)
GPIO.output(17, GPIO.HIGH)
time.sleep(1)
GPIO.output(17, GPIO.LOW)