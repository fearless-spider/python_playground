import requests

url = "https://a.klaviyo.com/api/flows/HwEq34/"

headers = {
    "accept": "application/json",
    "revision": "2024-07-15",
    "Authorization": "Klaviyo-API-Key",
}

response = requests.get(url, headers=headers)

print(response.text)