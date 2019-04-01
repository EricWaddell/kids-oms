from bottle import get, post, request, route, run, template
import json, configparser, requests
from random import random

config = configparser.ConfigParser()
config.read('config.ini')

this_host = config['EXCHANGE']['URL']
this_port = config['EXCHANGE']['PORT']

gateway_url = "http://" + config['GATEWAY']['URL'] + config['GATEWAY']['PORT']

base_prices = [
    {
        "name": "Coca Cola",
        "price": 50.5
    },
    {
        "name": "Nike",
        "price": 38.7
    }
]

market = [
    {
        "name": "Coca Cola",
        "quantity": 10,
        "price": 50.5
    },
    {
        "name": "Nike",
        "quantity": 10,
        "price": 38.7
    }
]


@post('/execute')
def execute():
    event = request.body.getvalue().decode('utf-8')
    jsonevent = json.loads(event)
    execution = get_execution(jsonevent)
    change_prices()
    print(market)
    return execution


def update_quantity(execution):
    global market
    instrument = next((x for x in market if x['name'] == execution['name']), None)
    if instrument is None:
        return
    else:
        instrument['quantity'] = instrument['quantity'] - execution['quantity']


def change_prices():
    global market
    global base_prices
    for instrument in market:
        base_price = next((x for x in base_prices if x['name'] == instrument['name']), None)
        if base_price is None:
            continue
        else:
            modifier = round(random()-.5, 2)
            instrument['price'] = base_price['price'] + modifier


def validate_event(event):
    global market
    instrument = next((x for x in market if x['name'] == event['name']), None)
    if instrument is None:
        return False
    if instrument['quantity'] < event['quantity']:
        return False
    else:
        return True


def get_execution(event):
    if validate_event(event):
        #if event['status'] == "buy"
        execution = {
            "status": "executed",
            "trader": event['trader'],
            "name": event['name'],
            "type": event['type'],
            "quantity": event['quantity']
        }
        update_quantity(execution)
        return json.dumps(execution)
    else:
        execution = {
            "status": "error",
            "trader": event['trader'],
            "name": event['name'],
            "type": event['type'],
            "quantity": event['quantity']
        }
        return json.dumps(execution)


run(host=this_host, port=this_port)