from datetime import date, timedelta
import csv
import requests
for f_type in ['pairs', 'prices']:
    c = csv.reader(requests.get('https://forecastex.com/api/download?date=' + (date.today()-timedelta(days=1)).strftime("%Y%m%d") + '&type=' + f_type).text.splitlines())
    with open(f_type + '.csv', 'w', newline='') as f:
        csv.writer(f).writerows(c)
