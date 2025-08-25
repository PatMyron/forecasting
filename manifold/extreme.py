import json
import requests
session = requests.Session()
response = session.get('https://api.manifold.markets/v0/bets').json()
bets = set()
markets = []
for bet in response:
  if bet['probAfter'] > .99 or bet['probAfter'] < .01:
    bets.add('https://api.manifold.markets/v0/market/' + bet['contractId'])
for bet in bets:
  response = session.get(bet).json()
  if response['outcomeType'] != "MULTIPLE_CHOICE" and response['outcomeType'] != "FREE_RESPONSE":
    markets.append(response)
print(json.dumps(markets, indent=1))
