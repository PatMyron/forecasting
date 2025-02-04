import json
import requests
from datetime import datetime, timedelta, UTC
url = 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=1000&status=open'
response = requests.get(url).json()
markets, unclosed, soon = [], [], []
while response:
  for market in response['markets']:
    unclosed.append(market)
    if datetime.fromisoformat(market['close_time']) < datetime.now(UTC) + timedelta(days=60):
      soon.append(market)
  if not response['cursor']:
    break
  response = requests.get(url + '&cursor=' + response['cursor']).json()
with open('open.json', 'w') as f:
  json.dump(unclosed, f, indent=0)
with open('soon.json', 'w') as f:
  json.dump(soon, f, indent=0)