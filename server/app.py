from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
import json
from bs4 import BeautifulSoup
import requests


app = app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


def get_text(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.text,"lxml")

    title = bs.find('h1', 'topic-body__titles')
    if title != None:
        title = title.text
    else:
        title = bs.find('h1', 'premium-header__titles').text
    main_text = " ".join([i.text for i in bs.find_all('p', 'topic-body__content-text')])

    text = title + ' ' + main_text

    return text


@app.route('/')
def index():
    return send_from_directory("static/", "index.html")


@socketio.event
def execute(message):
    j = json.loads(message)
    url = j["url"]

    text = get_text(url)
    target = "Россия,ВСУ"
    data = '{\n"model": "llama3",\n"prompt": "Answer Positively or NEGATIVELY based on how favourably you feel about %s in the following message. Rate based on format only. Give a rating of NEUTRAL if you think it is neutral: %s",\n"stream": true,\n"options": {\n"seed": 123,\n"top_k": 20,\n"top_p": 0.9,\n"temperature": 0\n}\n}' % (
    target, text)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    print(data)
    response = requests.post('http://ollama:11434/api/generate', headers=headers, data=data, stream=True)

    print(response, response.text)
    
    emit('result', str(response.body))


socketio.run(app, allow_unsafe_werkzeug=True)