from RPi import GPIO

GPIO.setmode(GPIO.BCM) # Choose BCM to use GPIO numbers instead of pin numbers
GPIO.setup(17, GPIO.IN)
while True:
    print(GPIO.input(17) == GPIO.LOW, end='\r')