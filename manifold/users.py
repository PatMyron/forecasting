import json
import requests
url = 'https://api.manifold.markets/v0/users?limit=1000'
response = requests.get(url).json()
users, whales, losers = [], [], []
while response:
  for user in response:
    users.append(user)
    if user['balance'] > 1000000:
      whales.append(user)
    if user.get('profitCached', {}).get('allTime', 0) < -200000: # https://manifold.markets/leaderboards
      losers.append(user)
  response = requests.get(url + '&before=' + response[-1]['id']).json()
with open('users.json', 'w') as f:
  json.dump(users, f, indent=0)
with open('whales.json', 'w') as f:
  json.dump(whales, f, indent=0)
with open('losers.json', 'w') as f:
  json.dump(losers, f, indent=0)
