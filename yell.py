#! /usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, sys, time, random
import BaseHTTPServer
from BeautifulSoup import BeautifulSoup

url = 'http://www.yell.com'
channel_classes = ['find-links']
advert_classes = ['advert-content']
address_classes = ['address']
phone_classes = ['advert-cta', 'fle-cta', 'advert-cta fle-cta']
category_classes = ['advert-footer', 'clearfix', 'advert-footer clearfix']
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'y', 'z']
global i
i = 0
p = open('proxy.csv', 'r')
proxies = p.readlines()
p.close()


def parseAddress(input):
    if input[:7] != 'http://':
        if input.find('://') != -1:
            print 'Error: Cannot retrive URL, address must be HTTP'
            sys.exit(1)
        else:
            input = 'http://' + input

    return input


def retrieveWebPage(address):
    try:
        web_handle = urllib2.urlopen(address)
    except urllib2.HTTPError, e:
        BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
        print 'Cannot retrieve URL: HTTP Error Code', e.code
        web_handle = False
    except urllib2.URLError, e:
        print 'Cannot retrieve URL: ' + e.reason[1]
        web_handle = False
    except:
        print 'Cannot retrieve URL: unknown error'
        sys.exit(1)
    return web_handle


def getNewProxy(proxyaddress):
    print proxyaddress
    proxy = urllib2.ProxyHandler({'http': proxyaddress})
    opener = urllib2.build_opener(proxy)
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
    urllib2.install_opener(opener)


for alp in alpha:
    page = None
    while page == None:
        try:
            getNewProxy(proxies[random.randint(0, 37)])
            page = urllib2.urlopen('http://www.yell.com/k/uk-' + alp + '.html')
        except urllib2.HTTPError, e:
            print 'Cannot retrieve URL: HTTP Error Code', e.code
            page = False
    soup = BeautifulSoup(page)
    f = open('data' + alp + '.csv', 'w')
    # f.write('%s' % f.read())
    l = open('log.txt', 'w')
    for channel in soup.findAll('ul'):
        if channel.has_key('class') and channel['class'] in channel_classes:

            for li in channel.findAll('li'):
                i = 0
                for a in li.findAll('a'):
                    noresult = False
                    href = str(a.get('href'))
                    l.write('%s' % href)
                    keywords = href[3:href.find('-')]
                    if keywords == 'a+plant':
                        print keywords
                        results = 10
                        startAt = 0
                        pageNum = 1
                        while True:
                            #                        time.sleep(random.randint(10,100))
                            plink = '/ucs/UcsSearchAction.do?startAt=' + str(
                                startAt) + '&keywords=' + keywords + '&location=uk&scrambleSeed=1602419087&searchType=advance&showOoa=10&ppcStartAt=0&pageNum=' + str(
                                pageNum)
                            results += 10
                            startAt += 10
                            pageNum += 1
                            print str(pageNum)
                            address = parseAddress(url + plink)
                            website_handle = False
                            while website_handle == False:
                                if i == len(proxies):
                                    i = 0
                                getNewProxy(proxies[i])
                                i = i + 1
                                website_handle = retrieveWebPage(address)

                            website_text = website_handle.read()
                            website_handle.close()

                            start = website_text.find('<div class="sort">')
                            if start == -1:
                                error = website_text.find('no-results')
                                if error != -1:
                                    print 'no result'
                                    noresult = True
                                    break
                                else:
                                    website_handle = False
                                    results -= 10
                                    startAt -= 10
                                    pageNum -= 1

                            website_text = website_text[start:]
                            end = website_text.find('<script type="text/javascript">')
                            #                        if i == 0:
                            #                            pstart = website_text.find('<div id="bottomPageNumbers">')
                            #                            pager_text = website_text[pstart:]
                            #                            pend = pager_text.find('</div>')
                            #                            pager_text = pager_text[0:pend]
                            website_text = website_text[0:end]

                            #                        if i == 0:
                            #                            pinner = BeautifulSoup(pager_text)
                            #                            for apager in pinner.findAll('a'):
                            #                                plink.append(str(apager.get('href')))

                            inner = BeautifulSoup(website_text)

                            phones = ''
                            href = ''
                            addresss = ''
                            title = ''
                            category = ''
                            for diva in inner.findAll('div'):
                                #                            time.sleep(random.randint(10,100))
                                if diva.has_key('class') and diva['class'] in advert_classes:
                                    for ahref in diva.findAll('a'):
                                        title = ahref.string
                                        href = str(ahref.get('href'))
                                    if title == '' or title == 'None':
                                        for ahref in diva.findAll('h2'):
                                            title = ahref.string
                                    for address in diva.findAll('span'):
                                        if address.has_key('class') and address['class'] in address_classes:
                                            for addr in address.contents:
                                                addresss += addr.string
                                if diva.has_key('class') and diva['class'] in phone_classes:
                                    for phone in diva.findAll('strong'):
                                        for pho in phone.contents:
                                            phones += pho.string + ';'
                                if diva.has_key('class') and diva['class'] in category_classes:
                                    for categories in diva.findAll('strong'):
                                        category = categories.contents[0].string
                                    f.write('%s;%s;%s%s;%s;\n' % (title, addresss, phones, category, href))
                                    print title
                                    phones = ''
                                    href = ''
                                    addresss = ''
                                    title = ''
                                    category = ''

    l.close()
    f.close()
print 'end'
page.close()
