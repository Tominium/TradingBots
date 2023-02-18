import urllib3
import requests
import json


url = 'https://www.yeezysupply.com/api/yeezysupply/products/bloom'
response = requests.get(url=url)
data = json.loads(response.content.decode('gzip'))

print(data)
