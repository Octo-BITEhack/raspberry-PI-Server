import time
from tools.sensors.pulse_oximetr import max30100
import threading


class PulsMeter:
    def __init__(self):
        self.mx30 = max30100.MAX30100()
        self.mx30.enable_spo2()

        self.last_spo2 = 0
        self.last_hb = 0

        self.__scheduled_read_running = True
        self.__scheduled_read_task = threading.Thread(target=self.__scheduled_read, args=())
        self.__scheduled_read_task.start()

        self.__registry = None
        self.__registry_going: bool = False
        self.__registry_delta: float = 0.3
        self.__registry_size: int = 30
        self.__registry_thread = None


    def __read_data(self):
        self.mx30.read_sensor()

        self.mx30.ir, self.mx30.red

        if self.mx30.ir == self.mx30.buffer_ir or self.mx30.ir == 0:
            hb = None
        else:
            hb = int(self.mx30.ir / 100)
        
        if self.mx30.red == self.mx30.buffer_red or self.mx30.red == 0:
            spo2 = None
        else:
            spo2 = int(self.mx30.red / 200)
        
        return hb, spo2

    def __scheduled_read(self, period=0.1):
        while self.__scheduled_read_running:
            hb, spo2 = self.__read_data()

            if hb != None:
                self.last_hb = hb
            
            if spo2 != None:
                self.last_spo2 = spo2
            
            time.sleep(period)

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
            self.__registry = [[], []]
        while self.__registry_going:
            self.__registry[0].append(self.get_pulse())
            self.__registry[1].append(self.get_saturation())
            if len(self.__registry[0]) > self.__registry_size:
                self.__registry[0] = self.__registry[0][:self.__registry_size]
                self.__registry[1] = self.__registry[1][:self.__registry_size]
            
            time.sleep(self.__registry_delta)
    
    def get_registry_puls(self):
        return self.__registry[0]
    
    def get_registry_spo2(self):
        return self.__registry[1]

    def get_pulse(self):
        return self.last_hb

    def get_saturation(self):
        return self.last_spo2

    def stop_register(self):
        self.__registry_going = False

    def __del__(self):
        self.__scheduled_read_running = False
        self.__registry_going = False
