import requests
from statistics import mean 
overall, paw, media = [], [], []
for market in requests.get('https://api.manifold.markets/v0/group/by-id/mGCdPei3RXTEoq1IGOAC/markets').json():
  overall.append(market['probability'])
  if market['question'].startswith('PAW'):
    paw.append(market['probability'])
  else:
    media.append(market['probability'])
print(mean(overall))
print('paw', mean(paw))
print('media', mean(media))