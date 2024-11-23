import json
import requests
url = 'https://manifold.markets/api/v0/users?limit=1000'
response = requests.get(url).json()
users, whales, losers = [], [], []
while response:
  for user in response:
    users.append(user)
    if user['balance'] > 100000:
      whales.append(user)
    if user['profitCached']['allTime'] < -15000:
      losers.append(user)
  response = requests.get(url + '&before=' + response[-1]['id']).json()
with open('users.json', 'w') as f:
  json.dump(users, f, indent=0)
with open('whales.json', 'w') as f:
  json.dump(whales, f, indent=1)
with open('losers.json', 'w') as f:
  json.dump(losers, f, indent=1)
