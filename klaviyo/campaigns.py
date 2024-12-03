import requests

url = "https://a.klaviyo.com/api/campaigns/?filter=equals%28messages.channel%2C%27sms%27%29"

headers = {
    "accept": "application/json",
    "revision": "2024-07-15",
    "Authorization": "Klaviyo-API-Key",
}

response = requests.get(url, headers=headers)

print(response.text)
