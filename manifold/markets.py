import json
import requests
import time
session = requests.Session()
url = 'https://api.manifold.markets/v0/markets?limit=1000'
response = session.get(url).json()
markets, unclosed, soon = [], [], []
while response:
  for market in response:
    markets.append(market)
    if not market['isResolved'] and market.get('closeTime', 0)/1000 > time.time():
      unclosed.append(market)
      if market.get('closeTime', 0)/1000 < time.time() + 2*30*24*60*60:
        soon.append(market)
  response = session.get(url + '&before=' + response[-1]['id']).json()
with open('all.json', 'w') as f:
  json.dump(markets, f, indent=0)
with open('open.json', 'w') as f:
  json.dump(unclosed, f, indent=0)
with open('soon.json', 'w') as f:
  json.dump(soon, f, indent=0)
