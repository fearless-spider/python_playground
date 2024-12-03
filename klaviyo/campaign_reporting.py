import requests

url = "https://a.klaviyo.com/api/campaign-values-reports/"

payload = {
    "data": {
        "type": "campaign-values-report",
        "attributes": {
            "statistics": ["average_order_value"],
            "timeframe": {"key": "last_12_months"},
            "conversion_metric_id": "KwmNnQ",
        },
    }
}
headers = {
    "accept": "application/json",
    "revision": "2024-07-15",
    "content-type": "application/json",
    "Authorization": "Klaviyo-API-Key",
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
