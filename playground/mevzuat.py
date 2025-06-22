import requests

url = "https://www.mevzuat.gov.tr/#kanunlar"
print(requests.get(url).text)
