import json
import os
import requests
from datetime import datetime, timedelta, UTC
from urllib3 import Retry
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=Retry(
  total=12,
  status_forcelist=[429],
  backoff_factor=0.1,
  backoff_jitter=0.2,
  backoff_max=2,
)))
url = 'https://www.metaculus.com/api2/questions/?limit=1000'
markets, unclosed, soon = [], [], []
while url:
  response = session.get(url, headers={'Authorization': 'Token ' + os.environ['METACULUS_KEY']}).json()
  for market in response['results']:
    markets.append(market)
    if market['status'] == 'open':
      unclosed.append(market)
      if datetime.fromisoformat(market['scheduled_close_time']) < datetime.now(UTC) + timedelta(days=60):
        soon.append(market)
  url = response['next']
with open('all.json', 'w') as f:
  json.dump(markets, f, indent=0)
with open('open.json', 'w') as f:
  json.dump(unclosed, f, indent=0)
with open('soon.json', 'w') as f:
  json.dump(soon, f, indent=1)