from flask import Flask, request
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
LOW_SATURATION_TRESHOLD = 85



pump_controller = gpio_controler.GPIOController(PUMP_GPIO)
fan_controller = gpio_controler.GPIOController(FAN_GPIO)

# global variables
global PULSE
global SATURATION
global IS_LIGHT
global IS_NOISE
global IS_HELMET_OPEN
global IS_BEER_BEING_DRANK
global IS_FUN_ON

PULSE = 100
SATURATION = 100
IS_LIGHT = True
IS_NOISE = False
IS_HELMET_OPEN = False
IS_BEER_BEING_DRANK = False
IS_FUN_ON = False

app = Flask(__name__)

# route
@app.route('/')
def home():
  return 'hey!'

@app.route('/stats', methods=['GET'])
def stats():
  global PULSE
  global SATURATION
  global IS_LIGHT
  global IS_NOISE
  global IS_HELMET_OPEN
  global IS_BEER_BEING_DRANK
  global IS_FUN_ON
  return {
    'pulse': PULSE,
    'saturation': SATURATION,
    'isLight': IS_LIGHT,
    'isNoise': IS_NOISE,
    'isHelmetOpen': IS_HELMET_OPEN,
    'isBeerBeingDrank': IS_BEER_BEING_DRANK,
    'isFunOn': IS_FUN_ON
  }

# @app.route('/helmet', methods=['POST'])
# def helmet():
#   global IS_HELMET_OPEN
#   if request.json['isHelmetOpen']:
#     fan_controller.turn_on()
#   else:
#     fan_controller.turn_off()
#   return str(IS_HELMET_OPEN)

@app.route('/fan', methods=['POST'])
def fan():
  global IS_FUN_ON
  IS_FUN_ON = request.json['isFanOn']
  if request.json['isFanOn']:
    fan_controller.turn_on()
  else:
    fan_controller.turn_off()
  return str(IS_FUN_ON)

@app.route('/beer', methods=['POST'])
def beer():
  global IS_BEER_BEING_DRANK
  IS_BEER_BEING_DRANK = request.json['isBeerBeingDrank']
  if request.json['isBeerBeingDrank']:
    fan_controller.turn_on()
  if not request.json['isBeerBeingDrank']:
    fan_controller.turn_off()
  return str(IS_BEER_BEING_DRANK)

def main_loop(puls_oximetr, light_sensor, sound_sensor, pump_controller, fan_controller):
    while True:
        global PULSE
        global SATURATION
        global IS_LIGHT
        global IS_NOISE
        global IS_HELMET_OPEN
        global IS_BEER_BEING_DRANK
        global IS_FUN_ON

        PULSE = puls_oximetr.get_pulse()
        SATURATION = puls_oximetr.get_saturation()
        IS_LIGHT = light_sensor.isLow()
        IS_NOISE = sound_sensor.isLow()
        # # IS_HELMET_OPEN = False
        # if  IS_BEER_BEING_DRANK and pump_controller.is_off:
        #     pump_controller.turn_on()
        # if (not IS_BEER_BEING_DRANK) and pump_controller.is_on:
        #     pump_controller.turn_off()
        
        # if  IS_FUN_ON and pump_controller.is_off:
        #     fan_controller.turn_on()
        # if (not IS_FUN_ON) and pump_controller.is_on:
        #     fan_controller.turn_off()

        if SATURATION < LOW_SATURATION_TRESHOLD:
          fan_controller.turn_on_for(5)


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
    # pump_controller = gpio_controler.GPIOController(PUMP_GPIO)
    # fan_controller = gpio_controler.GPIOController(FAN_GPIO)
    t = threading.Thread(target=main_loop, args=(puls_oximetr, light_sensor, sound_sensor, pump_controller, fan_controller))
    t.start()


# listen
if __name__ == "__main__":
    main()
    app.run(host='192.168.137.220', port=5000, debug=True)
