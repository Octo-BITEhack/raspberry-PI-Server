from flask import Flask

app = Flask(__name__)

# route
@app.route('/')
def home():
  return 'hey!'

# listen
if __name__ == "__main__":
  app.run(host='192.168.137.220', port=3000, debug=True)