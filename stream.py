from bottle import get, post, request, route, run, template
import json, configparser, requests

config = configparser.ConfigParser()
config.read('config.ini')

proxy_url = "http://" + config['PROXY']['URL'] + config['PROXY']['PORT']
gateway_url = "http://" + config['GATEWAY']['URL'] + config['GATEWAY']['PORT']

history = []

@post('/stream')
def post_event():
    global history
    body = request.body.getvalue().decode('utf-8')
    history.append(body)
    broadcast_event(body)

def broadcast_event(event):
    global history
    print(history)

@get('/stream/<eventid>')
def get_event(eventid):
    return "0"

run(host='localhost', port=8080)