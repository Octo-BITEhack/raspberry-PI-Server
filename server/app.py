from flask import Flask

# global variables
global PULSE = 100
global SATURATION = 100
global IS_LIGHT = True
global IS_NOISE = False
global IS_HELMET_OPEN = False
global IS_BEER_BEING_DRANK = False

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
  return 'ok'

@app.route('/beer', methods=['POST'])
def beer():
  IS_BEER_BEING_DRANK = request.json['isBeerBeingDrank']
  return 'ok'

# listen
if __name__ == "__main__":
  app.run(host='192.168.137.220', port=5000, debug=True)
