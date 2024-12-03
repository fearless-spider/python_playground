import json

import requests

url = "https://a.klaviyo.com/api/flows/?page%5Bcursor%5D=bmV4dDo6aWQ6OlZucWs4TQ"

headers = {
    "accept": "application/json",
    "revision": "2024-07-15",
    "Authorization": "Klaviyo-API-Key",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    json_data = json.loads(response.text)
    print(json_data)

    results_data = json_data["data"]
    data = []

    for result_data in results_data:
        data.append(
            {
                "id": result_data["id"],
                "name": result_data["attributes"]["name"],
                "status": result_data["attributes"]["status"],
            }
        )

    file = open("flows.json", "w")
    file.writelines("%s \n" % json.dumps(line) for line in data)
    file.close()
