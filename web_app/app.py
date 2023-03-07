from psutil import cpu_percent
from flask import Flask
from flask.json import jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"cpu_load": cpu_percent()})

if __name__ == "__main__":
    app.run()
