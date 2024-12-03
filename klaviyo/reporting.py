import json

import requests

url = "https://a.klaviyo.com/api/flow-series-reports/"

payload = {
    "data": {
        "type": "flow-series-report",
        "attributes": {
            "statistics": [
                "average_order_value",
                "bounce_rate",
                "bounced",
                "bounced_or_failed",
                "bounced_or_failed_rate",
                "click_rate",
                "click_to_open_rate",
                "clicks",
                "clicks_unique",
                "conversion_rate",
                "conversion_uniques",
                "conversion_value",
                "conversions",
                "delivered",
                "delivery_rate",
                "failed",
                "failed_rate",
                "open_rate",
                "opens",
                "opens_unique",
                "recipients",
                "revenue_per_recipient",
                "spam_complaint_rate",
                "spam_complaints",
                "unsubscribe_rate",
                "unsubscribe_uniques",
                "unsubscribes",
            ],
            "timeframe": {"key": "this_year"},
            "interval": "weekly",
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

if response.status_code == 200:
    json_data = json.loads(response.text)
    print(json_data)
    results_data = json_data["data"]["attributes"]["results"]
    results_datetime = json_data["data"]["attributes"]["date_times"]

    data = []

    for result_data in results_data:
        flow_id = result_data["groupings"]["flow_id"]
        send_channel = result_data["groupings"]["send_channel"]
        statistics = result_data["statistics"]

        counter = 0
        for date in results_datetime:
            d = {"datetime": date, "flow_id": flow_id, "send_channel": send_channel}
            for statistic in statistics:
                stats = statistics[statistic][counter]
                d.update({statistic: stats})
            counter += 1
            data.append(d)

    file = open("test.json", "w")
    file.writelines("%s \n" % json.dumps(line) for line in data)
    file.close()
