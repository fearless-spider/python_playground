'''
Created on 27-01-2011

@author: fearless-spider
'''

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re

count = 10000
emaillist = ''
while(True):
    print count
    profileUrl = 'http://randki.o2.pl/profile.php?id_r=' + str(count)
    response = urllib2.urlopen(profileUrl)
    if response is not None:
        page = response.read()
        start = page.find('<center>')
        end = page.find('</center>')
        page = page[start:end]
        soup = BeautifulSoup(page)
        for email in soup.findAll('a', href=re.compile('mailto:')):
            for content in email.findAll('u'):
                print content
                email = str(content)
                emaillist = emaillist + email[3:email.find('</')] + ',\n\r'

    count = count + 1
    if count > 1600:
        break
FILE = open('emaillist.csv', 'a')
FILE.write(emaillist)
FILE.close()
