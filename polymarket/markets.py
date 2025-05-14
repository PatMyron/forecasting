import json
import requests
import requests_cache
from datetime import datetime, timedelta, UTC
requests_cache.install_cache('cache')
offset = 0
markets, unclosed, soon = [], [], []
while requests.get('https://gamma-api.polymarket.com/markets?limit=500&offset=' + str(offset)).json():
  for market in requests.get('https://gamma-api.polymarket.com/markets?limit=500&offset=' + str(offset)).json():
    markets.append(market)
    if not market['closed']:
      unclosed.append(market)
      try:
        if datetime.fromisoformat(market['endDate']) < datetime.now(UTC) + timedelta(days=60):
          soon.append(market)
      except:
        try:
          if datetime.fromisoformat(market['events'][0]['endDate']) < datetime.now(UTC) + timedelta(days=60):
            soon.append(market)
        except:
          pass
  offset += 500
with open('all.json', 'w') as f:
  json.dump(markets, f, indent=0)
with open('open.json', 'w') as f:
  json.dump(unclosed, f, indent=0)
with open('soon.json', 'w') as f:
  json.dump(soon, f, indent=0)
