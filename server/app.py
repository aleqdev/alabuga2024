from flask import Flask, send_from_directory, request


app = app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory("static/", "index.html")


@app.route("/execute", methods=["GET", 'POST'])
def execute():
    json = request.json
    print(json)

    return {"ok": 1}