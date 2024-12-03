import requests
import csv


def get_bounces(url=None):
    print(url)
    if url:
        return requests.get(
            url,
            auth=("api", ""))
    return requests.get(
        "https://api.mailgun.net/v3/example.net/bounces?limit=5000",
        auth=("api", ""))


if __name__ == '__main__':
    nextUrl = "https://api.mailgun.net/v3/example.net/bounces?limit=5000"
    csvData = [['Email', 'Bounce']]
    while nextUrl:
        r = get_bounces(nextUrl)
        if r.status_code == 200:
            data = r.json()
            nextUrl = data.get('paging').get('next', False)
            items = data.get('items')
            for item in items:
                csvData.append([item.get('address'), True])
            if nextUrl.find('page') == -1:
                nextUrl = None
                with open('bounces.csv', 'w') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerows(csvData)

                csvFile.close()
        else:
            print(r)
