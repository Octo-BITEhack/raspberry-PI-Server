from flask import Flask
from tools.sensors import gpio_inputs
from tools.sensors.pulse_oximetr import puls_meter
from tools.controllers import gpio_controler
import threading, time

# constans PARAMS
LIGHT_GPIO = 27
SOUND_GPIO = 22
PUMP_GPIO = 17 
FAN_GPIO = 18
MAIN_PERIOD = 1

# global variables
global PULSE
global SATURATION
global IS_LIGHT
global IS_NOISE
global IS_HELMET_OPEN
global IS_BEER_BEING_DRANK

PULSE = 100
SATURATION = 100
IS_LIGHT = True
IS_NOISE = False
IS_HELMET_OPEN = False
IS_BEER_BEING_DRANK = False

app = Flask(__name__)

# route
@app.route('/')
def home():
  return 'hey!'

@app.route('/stats', methods=['GET'])
def stats():
  return {
    'pulse': PULSE,
    'saturation': SATURATION,
    'isLight': IS_LIGHT,
    'isNoise': IS_NOISE,
    'isHelmetOpen': IS_HELMET_OPEN,
    'isBeerBeingDrank': IS_BEER_BEING_DRANK
  }

@app.route('/helmet', methods=['POST'])
def helmet():
  IS_HELMET_OPEN = request.json['isHelmetOpen']
  return 200, 'ok'

@app.route('/beer', methods=['POST'])
def beer():
  IS_BEER_BEING_DRANK = request.json['isBeerBeingDrank']
  return 200, 'ok'

def main_loop(puls_oximetr, light_sensor, sound_sensor, pump_controller):
    while True:
        PULSE = puls_oximetr.get_pulse()
        SATURATION = puls_oximetr.get_saturation()
        IS_LIGHT = light_sensor.isHigh()
        IS_NOISE = sound_sensor.isHigh()
        # IS_HELMET_OPEN = False
        if  IS_BEER_BEING_DRANK and pump_controller.is_off:
            pump_controller.turn_on()
        if (not IS_BEER_BEING_DRANK) and pump_controller.is_on:
            pump_controller.turn_off()

        print({
            'pulse': PULSE,
            'saturation': SATURATION,
            'isLight': IS_LIGHT,
            'isNoise': IS_NOISE,
            'isHelmetOpen': IS_HELMET_OPEN,
            'isBeerBeingDrank': IS_BEER_BEING_DRANK
        })
        time.sleep(MAIN_PERIOD)

def main():
    puls_oximetr = puls_meter.PulsMeter()
    light_sensor = gpio_inputs.GPIO_input(LIGHT_GPIO)
    sound_sensor = gpio_inputs.GPIO_input(SOUND_GPIO)
    pump_controller = gpio_controler.GPIOController(PUMP_GPIO)
    t = threading.Thread(target=main_loop, args=(puls_oximetr, light_sensor, sound_sensor, pump_controller))
    t.start()


# listen
if __name__ == "__main__":
    main()
    app.run(host='192.168.137.220', port=5000, debug=True)
