from RPi import GPIO
import time, sys, threading

GPIO.setmode(GPIO.BCM)

class GPIO_input:
    def __init__(self, gpio_num):
        self.GPIO_NUM = gpio_num        
        GPIO.setup(gpio_num, GPIO.IN)
        self.__registry = None
        self.__registry_going: bool = False
        self.__registry_delta: float = 0.1
        self.__registry_size: int = 30
        self.__registry_thread = None

    
    def isLow(self):
        return GPIO.input(self.GPIO_NUM) == GPIO.LOW

    def isHigh(self):
        return GPIO.input(self.GPIO_NUM) == GPIO.HIGH
    
    def beginRegister(self, delta_time=0.1, history_size=30):
        self.__registry_delta = delta_time
        self.__registry_size = history_size
        if self.__registry_going:
            return

        self.__registry_going = True
        self.__registry_thread = threading.Thread(target=self.__registry_thread_func, args=())
        self.__registry_thread.start()


        
    def __registry_thread_func(self):
        if self.__registry is None:
            self.__registry = []
        while self.__registry_going:
            self.__registry.append(1 if self.isHigh() else 0)
            time.sleep(self.__registry_delta)
            if len(self.__registry) > self.__registry_size:
                self.__registry = self.__registry[:self.__registry_size]

    def get_registry(self):
        return self.__registry

    def stop_register(self):
        self.__registry_going = False

    def __del__(self):
        self.__registry_going = False

        

