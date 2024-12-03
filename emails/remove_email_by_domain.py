import csv

with open('emails.csv', 'rb') as inp, open('bounces_emails.csv', 'wb') as out, open('bounces.csv', 'rb') as bounced:
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
        add = False
        for bounce in bounced_emails:
            if email.find("@" + bounce) != -1:
                add = True
                break
        if add:
            print(email)
            row = [email, 1]
            writer.writerow(row)
