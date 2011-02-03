'''
Created on 25-01-2011

@author: fearless-spider
'''
import csv

listing = csv.reader(open('south-dakotacat.csv', 'rb'), delimiter='^', quotechar='~')
catlisting = csv.reader(open('category.csv', 'rb'), delimiter='^', quotechar='~')
categoryWriter = csv.writer(open('categorynew.csv', 'wb'), delimiter='^', quotechar='~')

# categoryWriter.writerow(['category_name'])
newrow = []
for newrow in listing:
    rows = []
    row = []
    print newrow[0]
    for row in catlisting:
        if newrow[0].lower() == row[0].lower():
            rows.append(row[0])
            categoryWriter.writerow(rows)
        print row[0]
