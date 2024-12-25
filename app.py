from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """<!DOCTYPE html>
    <html>
    <body>

    <h1>My First Heading</h1>
    <p>My first paragraph.</p>

    </body>
    </html>"""

@app.route('/test')
def test():
    return 'This is a test!'

if __name__ == '__main__':
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 33507))
    app.run(host=host, port=port, debug=True)
