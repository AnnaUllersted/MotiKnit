from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Heroku!'

if __name__ == '__main__':
    host = "0.0.0.0"
    app.run(host=host, debug=True)
