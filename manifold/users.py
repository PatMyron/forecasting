import json
import requests
from urllib3 import Retry
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=Retry(
  total=12,
  status_forcelist=[429],
  backoff_factor=0.1,
  backoff_jitter=0.2,
  backoff_max=2,
)))
url = 'https://api.manifold.markets/v0/users?limit=1000'
response = session.get(url).json()
users, whales, losers = [], [], []
while response:
  for user in response:
    users.append(user)
    if user['balance'] > 1000000:
      whales.append(user)
    if user.get('profitCached', {}).get('allTime', 0) < -200000: # https://manifold.markets/leaderboards
      losers.append(user)
  response = session.get(url + '&before=' + response[-1]['id']).json()
with open('users.json', 'w') as f:
  json.dump(users, f, indent=0)
with open('whales.json', 'w') as f:
  json.dump(whales, f, indent=0)
with open('losers.json', 'w') as f:
  json.dump(losers, f, indent=0)
