from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Heroku!'

if __name__ == '__main__':
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 33507))
    app.run(host=host, port=port, debug=True)
