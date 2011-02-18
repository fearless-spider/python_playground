# -*- coding: utf-8 -*-
import traceback
import urllib2
import simplejson
from statsdb import db_close, db_open, update_twitter_team, get_twitter_teams_null

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'Accept': 'text/html', 'User-Agent': user_agent}

cc = db_open()
c = cc[0]
conn = cc[1]

teams = get_twitter_teams_null(c)

for team in teams:
    try:
        print team[1]
        url = 'http://api.twitter.com/1/statuses/user_timeline/' + team[1] + '.json'
        req = urllib2.Request(url=url, headers=headers)
        res = urllib2.urlopen(req)
    except:
        print traceback.format_exc()
    else:
        feed = res.read()

        decode_feed = simplejson.loads(feed)

        if len(decode_feed):
            twitter_id = decode_feed[0]['user']['id_str']
            print twitter_id
            if twitter_id:
                update_twitter_team(c, twitter_id, team[0])

db_close(c, conn)
