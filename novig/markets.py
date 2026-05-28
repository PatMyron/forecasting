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

markets = session.get('https://api.novig.us/nbx/v2/emm/markets/open').json()
leagues = {}

for market in markets:
  league = market.get('event', {}).get('game', {}).get('league') or 'UNKNOWN'
  leagues.setdefault(league, 0)
  leagues[league] += 1

with open('open.json', 'w') as f:
  json.dump(markets, f, indent=0)

with open('leagues.json', 'w') as f:
  json.dump(dict(sorted(leagues.items())), f, indent=0)
