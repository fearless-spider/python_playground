'''
Created on c

@author: fearless-spider
'''

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re

for age in range(22,60):
    print age
    data = urllib.urlencode({
                         'forma':'short_search',
                         'miejscowosc':'',
                         'plec':'2',
                         'szukaj.x':'104',
                         'szukaj.y':'8',
                         'wiek1':age,
                         'wiek2':age,
                         'wojewodztwo_panstwo':'6'
                         })
    req = urllib2.Request('http://randki.o2.pl/szukaj.php', data)
    count = 0
    emaillist = ''
    while(True):
        print count
        if count > 0:
            req = 'http://randki.o2.pl/szukaj.php?id_s=42355552&start='+str(count)+'&f=short_search&sort='
        response = urllib2.urlopen(req)
        page = response.read()
        start = page.find('<center>')
        end = page.find('</center>')
        page = page[start:end]
        soup = BeautifulSoup(page)
    
        for profile in soup.findAll('a', {'target':"_blank",'style':"font-size: 14px"}):
            #print profile['href']
            profileUrl = 'http://randki.o2.pl' + profile['href']
            response = urllib2.urlopen(profileUrl)
            page = response.read()
            start = page.find('<center>')
            end = page.find('</center>')
            page = page[start:end]
            soup = BeautifulSoup(page)
            for email in soup.findAll('a', href=re.compile('mailto:')):
                for content in email.findAll('u'):
#                if content.find('<u>') is None:
#                    break
                    print content
                    email = str(content)
                    emaillist = emaillist + email[3:email.find('</')] + ',\n\r'

        count = count + 10
        if count > 1500:
            break
    FILE = open('emaillist.csv', 'a')
    FILE.write(emaillist)
    FILE.close()
    age = age + 1

