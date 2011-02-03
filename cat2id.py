#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv

listing = csv.reader(open('alaska.csv', 'rb'), delimiter='^', quotechar='~')
listingWriter = csv.writer(open('alaskaid.csv', 'wb'), delimiter='^', quotechar='~')
rows = []
cat = 0
for row in listing:
    newrow = []
    rowcat = None
    listingcat = csv.reader(open('category.csv', 'rb'), delimiter='^', quotechar='~')
    for rowcat in listingcat:
        if row[4] == rowcat[0]:
            cat = rowcat[1]
            print row[4]
            break

    newrow.append(str(row[0]))
    newrow.append(row[1])
    newrow.append(row[2])
    newrow.append(row[3])
    newrow.append(cat)
    newrow.append(row[5])
    newrow.append(row[6])
    rows.append(newrow)
listingWriter.writerows(rows)
