import csv

domains = []
out = open('SubscriptionBox_Domains_Dec_2020.csv', 'a')
writer = csv.writer(out)
writer.writerow(['Domain'])
for i in range(1, 6, 1):
    with open('outreach'+str(i)+'.csv', 'rb') as inp:
        rows = csv.reader(inp)
        for row in rows:
            if row[0] != "":
                domain = row[0].replace('"', '').replace('http://', '').replace('https://', '').replace('www.', '').replace('\\', '')
                if domain.find('/') != -1:
                    domain = domain[0:domain.find('/')]
                if domain.find('?') != -1:
                    domain = domain[0:domain.find('?')]
                if domain.find('.') != -1 and domain not in domains:
                    print domain
                    domains.append(domain)
                    row_o = [domain]
                    writer.writerow(row_o)
out.close()
