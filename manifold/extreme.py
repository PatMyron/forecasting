import json
import requests
response = requests.get('https://manifold.markets/api/v0/bets').json()
bets = set()
markets = []
for bet in response:
  if bet['probAfter'] > .99 or bet['probAfter'] < .01:
    bets.add('https://manifold.markets/api/v0/market/' + bet['contractId'])
for bet in bets:
  response = requests.get(bet).json()
  if response['outcomeType'] != "MULTIPLE_CHOICE" and response['outcomeType'] != "FREE_RESPONSE":
    markets.append(response)
print(json.dumps(markets, indent=1))
