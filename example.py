from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask server is running"

def run():
    app.run(host="0.0.0.0", port=8080, debug=False)

def example():
    thread = Thread(target=run)
    thread.daemon = True
    thread.start()