from flask import Flask
from tools.sensors import gpio_inputs
from tools.sensors.puls_meter import puls_meter
import threading

# constans PARAMS
LIGHT_GPIO = 17
SOUND_GPIO = 21 

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

def main_loop(puls_oximetr, light_sensor, sound_sensor):
    while True:
        PULSE = puls_oximetr.get_pulse()
        SATURATION = puls_oximetr.get_saturation()
        IS_LIGHT = light_sensor.isHigh()
        IS_NOISE = sound_sensor.isHigh()
        # IS_HELMET_OPEN = False
        # IS_BEER_BEING_DRANK = False

def main():
    puls_oximetr = puls_meter.PulsMeter()
    light_sensor = gpio_inputs.GPIO_input(LIGHT_GPIO)
    sound_sensor = gpio_inputs.GPIO_input(SOUND_GPIO)
    t = threading.Thread(target=main_loop, args=(puls_oximetr, light_sensor, sound_sensor))
    t.start()


# listen
if __name__ == "__main__":
    main()
    app.run(host='192.168.137.220', port=5000, debug=True)
