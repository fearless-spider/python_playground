import csv

aliases = ['admin', 'info', 'sales', 'contact']

with open('domains_outreach.csv', 'rb') as inp, open('SubscriptionBox_Alias_Emails_Dec_2020.csv', 'wb') as out:
    writer = csv.writer(out)
    writer.writerow(['Email'])
    rows = csv.reader(inp)
    for row in rows:
        if row[0] != "Domain":
            for alias in aliases:
                email = alias + '@' + row[0]
                print(email)
                rowo = [email]
                writer.writerow(rowo)
