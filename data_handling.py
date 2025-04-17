import requests
import os

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={STOCK_API_KEY}'
r = requests.get(url)
data = r.json()

print(data)