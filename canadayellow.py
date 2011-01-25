#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25-01-2011

@author: fearless-spider
'''

import urllib2, sys, time, random
import BaseHTTPServer
import csv
from BeautifulSoup import BeautifulSoup
from htmlentitydefs import name2codepoint as n2cp
import re

def substitute_entity(match):
    ent = match.group(2)
    if match.group(1) == "#":
        return unichr(int(ent))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute_entity, string)[0]

listingWriter = csv.writer(open('datak.csv','wb'), delimiter='^', quotechar='~')
url = 'http://www.yell.com'
channel_id = ['geoListings']
adverts_class = ['listingDetail']
span_class = ['listingTitle']
phone_class = ['phoneNumber']
address_class = ['address']
category_class = ['ypgCategoryLink']
web_class = ['noPrint']
advertsphone_class = ['listingDetailRHS']
for pagenr in range(1,51):
    print pagenr
    page = urllib2.urlopen('http://www.yellowpages.ca/search/si/'+str(pagenr)+'/k/Canada')

    website_content = page.read()
    start = website_content.find('<div id="geoListings">')
    website_content = website_content[start:]
    end = website_content.find('<div id="rightPane">')
    website_content = website_content[:end]
    while True:
        sstart = website_content.find('<script')
        if sstart == -1:
            break
        send = website_content.find('</script>')
        website_content = website_content[:sstart] + website_content[send+9:]

    soup = BeautifulSoup(website_content)
    for channel in soup.findAll('div'):
        if channel.has_key('id') and channel['id'] in channel_id:
            for adverts in channel.findAll('div'):
                title = ''
                phone = ''
                category = ''
                address = ''
                web = ''
                if adverts.has_key('class') and adverts['class'] in adverts_class:
                    row = []
                    for span in adverts.findAll('span'):
                        if span.has_key('class') and span['class'] in span_class:
                            title = str(span.string).strip().decode('utf-8')
                            row.append(title)
                        if span.has_key('class') and span['class'] in category_class:
                            for ahref in span.findAll('a'):
                                category = ahref.string
                    row.append(category.strip().replace('&amp;', '&'))
                            #print category
                if adverts.has_key('class') and adverts['class'] in advertsphone_class:
                    for ahref in adverts.findAll('a'):
                        if ahref.has_key('class') and ahref['class'] in phone_class:
                            phone = ahref.string
                            row.append(decode_htmlentities(phone.strip()))
                if adverts.has_key('class') and adverts['class'] in address_class:
                    address = adverts.string
                    row.append(address.decode('utf-8').strip())
                if adverts.has_key('class') and adverts['class'] in web_class:                    
                    for ahref in adverts.findAll('a'):
                        web = str(ahref.get('title')).strip().decode('utf-8')
                        if web.find('www') != -1:
                            web = web[web.find('www'):web.rfind('-')-1]
                            row.append(web.strip())
                    listingWriter.writerow(row)
    page.close()
