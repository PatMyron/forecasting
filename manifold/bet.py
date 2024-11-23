import json
import os
import requests
body = {
    "contractId": "NEpTIkMlf9EZY9PBTyB3",
    "amount": 1,
    "outcome": "YES",
    "limitProb": 0.01
}
headers = {
    "Authorization": f"Key {os.getenv('API_KEY')}"
}
print(requests.post('https://manifold.markets/api/v0/bet', json=body, headers=headers).json())
