import csv

with open('domains.csv', 'rb') as inp, open('clean_domains.csv', 'wb') as out, open('bounces.csv', 'rb') as bounced:
    writer = csv.writer(out)
    rows = csv.reader(inp)
    bounced = csv.reader(bounced)
    emails = []
    bounced_emails = []
    for row in rows:
        emails.append(row[0].replace('"', ''))
    for bounce in bounced:
        if len(bounce) > 0:
            bounced_emails.append(bounce[0])
    for email in emails:
        add = True
        for bounce in bounced_emails:
            if email.find(bounce) != -1:
                add = False
                break
        if add:
            print(email)
            row = [email]
            writer.writerow(row)
