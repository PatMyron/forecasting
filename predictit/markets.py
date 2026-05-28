import json
import requests
import xml.etree.ElementTree as ET
from urllib3 import Retry

session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=Retry(
  total=12,
  status_forcelist=[429],
  backoff_factor=0.1,
  backoff_jitter=0.2,
  backoff_max=2,
)))


def child_text(element, name):
  child = element.find('{*}' + name)
  return child.text if child is not None else None


def maybe_float(value):
  try:
    return float(value)
  except (TypeError, ValueError):
    return value


response = session.get('https://www.predictit.org/api/marketdata/all/')
root = ET.fromstring(response.content)
markets, open_markets = [], []

for market in root.findall('.//{*}MarketData'):
  parsed_market = {
    'id': child_text(market, 'ID'),
    'name': child_text(market, 'Name'),
    'shortName': child_text(market, 'ShortName'),
    'url': child_text(market, 'URL'),
    'image': child_text(market, 'Image'),
    'status': child_text(market, 'Status'),
    'timestamp': child_text(market, 'TimeStamp'),
    'contracts': [],
  }

  contracts = market.find('{*}Contracts')
  if contracts is not None:
    for contract in contracts.findall('{*}MarketContract'):
      parsed_market['contracts'].append({
        'id': child_text(contract, 'ID'),
        'name': child_text(contract, 'Name'),
        'shortName': child_text(contract, 'ShortName'),
        'dateEnd': child_text(contract, 'DateEnd'),
        'image': child_text(contract, 'Image'),
        'status': child_text(contract, 'Status'),
        'lastTradePrice': maybe_float(child_text(contract, 'LastTradePrice')),
        'bestBuyYesCost': maybe_float(child_text(contract, 'BestBuyYesCost')),
        'bestBuyNoCost': maybe_float(child_text(contract, 'BestBuyNoCost')),
        'bestSellYesCost': maybe_float(child_text(contract, 'BestSellYesCost')),
        'bestSellNoCost': maybe_float(child_text(contract, 'BestSellNoCost')),
      })

  markets.append(parsed_market)
  if parsed_market['status'] == 'Open':
    open_markets.append(parsed_market)

with open('all.json', 'w') as f:
  json.dump(markets, f, indent=0)

with open('open.json', 'w') as f:
  json.dump(open_markets, f, indent=0)
