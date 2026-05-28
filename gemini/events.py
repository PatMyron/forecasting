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

base_url = 'https://api.gemini.com/v1/prediction-markets/events'
limit = 100
offset = 0
events = []

while True:
  response = session.get(base_url + '?limit=' + str(limit) + '&offset=' + str(offset)).json()
  events.extend(response['data'])
  pagination = response.get('pagination', {})
  offset += pagination.get('limit', limit)
  if offset >= pagination.get('total', len(events)):
    break

categories = session.get('https://api.gemini.com/v1/prediction-markets/categories').json()

with open('events-open.json', 'w') as f:
  json.dump(events, f, indent=0)

with open('categories.json', 'w') as f:
  json.dump(categories, f, indent=0)
