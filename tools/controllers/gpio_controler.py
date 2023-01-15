from RPi import GPIO
import time, threading

GPIO.setmode(GPIO.BCM)

class GPIOController:
    def __init__(self, gpio_num):
        self.GPIO_NUM = gpio_num
        GPIO.setup(self.GPIO_NUM, GPIO.OUT)
        self.default_turn_off = GPIO.HIGH
        self.default_turn_on = GPIO.LOW
        self.turn_off()
        self.is_on = False

    def turn_on(self):
        GPIO.output(self.GPIO_NUM, self.default_turn_on)
        self.is_on = True

    def turn_off(self):
        GPIO.output(self.GPIO_NUM, self.default_turn_off)
        self.is_on = False

    def turn_on_for(self, period):
        self.turn_on()
        t = threading.Thread(target=self.__turn_off_after, args=[period])
        t.start()

    def __turn_off_after(self, period):
        time.sleep(period)
        self.turn_off()