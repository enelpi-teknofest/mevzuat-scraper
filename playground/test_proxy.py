import requests

# Target URL
url = "https://httpbin.org/ip"  # This service returns your public IP

# Proxy configuration
proxies = {
    "http": "http://oc-7a572446969ee5c24ffbe8a8ed851cf24600b41a9d898982dbb70c435ec59fbb-country-TR-session-d9242:v1leozow6ges@proxy.oculus-proxy.com:31111",
    "https": "http://oc-7a572446969ee5c24ffbe8a8ed851cf24600b41a9d898982dbb70c435ec59fbb-country-TR-session-d9242:v1leozow6ges@proxy.oculus-proxy.com:31111"
}

# Optional: If your proxy requires authentication
# proxies = {
#     "http": "http://username:password@your_proxy_ip:your_proxy_port",
#     "https": "http://username:password@your_proxy_ip:your_proxy_port"
# }

try:
    response = requests.get(url, proxies=proxies, timeout=10)
    print("Response via Proxy:", response.text)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
