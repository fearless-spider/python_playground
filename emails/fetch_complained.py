import requests
import csv


def get_bounces(url):
    return requests.get(
        url,
        auth=("api", ""), params={"event": "complained"})


if __name__ == '__main__':
    nextUrl = "https://api.mailgun.net/v3/example.net/events"
    with open('complained.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        csvData = [['Email', 'Bounce']]
        i = 0
        while nextUrl:
            if i == 1000:
                break
            r = get_bounces(nextUrl)
            if r.status_code == 200:
                data = r.json()
                nextUrl = data.get('paging').get('next', False)
                print(nextUrl)
                items = data.get('items')

                for item in items:
                    csvData.append([item.get('recipient'), True])
            i += 1

        writer.writerows(csvData)

        csvFile.close()
