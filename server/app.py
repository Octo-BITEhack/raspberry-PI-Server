from flask import Flask

app = Flask(__name__)

# route
@app.route('/')
def home():
  return 'hey!'

# listen
if __name__ == "__main__":
  app.run(port=3000, debug=True)