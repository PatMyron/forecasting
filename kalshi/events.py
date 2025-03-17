import json
import requests
url = 'https://api.elections.kalshi.com/trade-api/v2/events?limit=200&status=open&cursor='
response = requests.get(url).json()
unclosed = []
while response:
  for e in response['events']:
    unclosed.append(e)
  if not response['cursor']:
    break
  response = requests.get(url + response['cursor']).json()
with open('events-open.json', 'w') as f:
  json.dump(unclosed, f, indent=0)