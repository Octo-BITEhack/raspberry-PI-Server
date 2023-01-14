#!/usr/bin/env python3

# AM2320 PINOUT to Raspberry Pi 4B GPIO pins 
# ╔═════════╗
# ║╬╬╬╬╬╬╬╬╬║
# ║╬╬╬╬╬╬╬╬╬║
# ║         ║
# ║ 1 2 3 4 ║
# ╚═╪═╪═╪═╪═╝
#   │ │ │ │                    | Raspberry Pi pins
#   │ │ │ └─ SCL = GPIO 3(SCL) | pin #5
#   │ │ └─ GND = Ground        | pin #9
#   │ └─  SDA = GPIO 2(SDA)    | pin #3
#   └─ VDD = 3v3 power         | pin #1

# pip3 install adafruit-circuitpython-am2320
# pip3 install adafruit-blinka
# Read more at https://learn.adafruit.com/adafruit-am2320-temperature-humidity-i2c-sensor        

import time
import board
import busio
import adafruit_am2320
from signal import signal, SIGINT
from sys import exit

# create the I2C shared bus
i2c = busio.I2C(board.SCL, board.SDA)
am = adafruit_am2320.AM2320(i2c)

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print('Running. Press CTRL-C twice to exit.')
    while True:
        try:
            degreesF = ((am.temperature * 1.8) + 32)
            print("\r Temperature: {0:.2f}°F Humidity: {1:.2f}%".format(round(degreesF,1), round(am.relative_humidity,1)), end='')
            time.sleep(2)
        except:
            print("\r Trying again                                  ", end='')
            time.sleep(.5)