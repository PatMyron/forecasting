import json
import requests
from datetime import datetime, timedelta, UTC
session = requests.Session()
url = 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=1000&status=open'
response = session.get(url).json()
markets, unclosed, soon, sooner, soonest = [], [], [], [], []
while response:
  for market in response['markets']:
    unclosed.append(market)
    if datetime.fromisoformat(market['close_time']) < datetime.now(UTC) + timedelta(days=60):
      soon.append(market)
    if datetime.fromisoformat(market['close_time']) < datetime.now(UTC) + timedelta(days=8):
      sooner.append(market)
    if datetime.fromisoformat(market['close_time']) < datetime.now(UTC) + timedelta(days=4):
      soonest.append(market)
  if not response['cursor']:
    break
  response = session.get(url + '&cursor=' + response['cursor']).json()
with open('open.json', 'w') as f:
  json.dump(unclosed, f, indent=0)
with open('soon.json', 'w') as f:
  json.dump(soon, f, indent=0)
with open('sooner.json', 'w') as f:
  json.dump(sooner, f, indent=0)
with open('soonest.json', 'w') as f:
  json.dump(soonest, f, indent=0)
