import json
import requests
session = requests.Session()
url = 'https://api.elections.kalshi.com/trade-api/v2/events?limit=200&status=open&cursor='
response = session.get(url).json()
unclosed = []
while response:
  for e in response['events']:
    vol = 0
    for m in session.get('https://api.elections.kalshi.com/trade-api/v2/events/' + e['event_ticker']).json()['markets']:
      vol += m['volume']
    e['volume'] = vol
    unclosed.append(e)
  if not response['cursor']:
    break
  response = session.get(url + response['cursor']).json()
with open('events-open.json', 'w') as f:
  json.dump(unclosed, f, indent=0)