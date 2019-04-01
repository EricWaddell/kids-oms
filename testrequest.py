import requests, json

url = "http://localhost:8085/execute"
data = {
    "status": "requested",
    "trader": "Eric",
    "name": "Coca Cola",
    "type": "market",
    "quantity": 5
}
headers = {"Content-type": "application/json"}
r = requests.post(url, data=json.dumps(data), headers=headers)
print(r.text)