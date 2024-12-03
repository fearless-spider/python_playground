import requests

url = "https://a.klaviyo.com/api/campaigns/01G65X758HXJFSMB8C8BXMQW0R/tags/"

headers = {
    "accept": "application/json",
    "revision": "2024-07-15",
    "Authorization": "Klaviyo-API-Key",
}

response = requests.get(url, headers=headers)

print(response.text)
