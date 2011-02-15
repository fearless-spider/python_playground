# -*- coding: utf-8 -*-
'''
@author: bespider
'''
import MySQLdb
from email.utils import parsedate_tz
import urllib2
import simplejson
import time
import feedparser
import re
from datetime import datetime, timedelta
import os.path
import sys
import socket


def get_twitter(url, limit=3):
    """Takes a twitter rss feed and returns a list of dictionaries, one per
    tweet. Each dictionary contains two attributes:
        - An html ready string with the @, # and links parsed to the correct
        html code
        - A datetime object of the posted date"""

    twitter_entries = []
    for entry in feedparser.parse(url)['entries'][:limit]:

        # convert the given time format to datetime
        posted_datetime = datetime.datetime(
            entry['updated_parsed'][0],
            entry['updated_parsed'][1],
            entry['updated_parsed'][2],
            entry['updated_parsed'][3],
            entry['updated_parsed'][4],
            entry['updated_parsed'][5],
            entry['updated_parsed'][6],
        )

        # format the date a bit
        if posted_datetime.year == datetime.datetime.now().year:
            posted = posted_datetime.strftime("%b %d")
        else:
            posted = posted_datetime.strftime("%b %d %y")

        # strip the "<username>: " that preceeds all twitter feed entries
        text = re.sub(r'^\w+:\s', '', entry['title'])

        # parse links
        text = re.sub(
            r"(http(s)?://[\w./?=%&\-]+)",
            lambda x: "<a href='%s'>%s</a>" % (x.group(), x.group()),
            text)

        # parse @tweeter
        text = re.sub(
            r'@(\w+)',
            lambda x: "<a href='http://twitter.com/%s'>%s</a>" \
                      % (x.group()[1:], x.group()),
            text)

        # parse #hashtag
        text = re.sub(
            r'#(\w+)',
            lambda x: "<a href='http://twitter.com/search?q=%%23%s'>%s</a>" \
                      % (x.group()[1:], x.group()),
            text)

        twitter_entries.append({
            'text': text,
            'posted': posted,
        })

    return twitter_entries


def get_twitter_date(date_str):
    time_tuple = parsedate_tz(date_str.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=3600 * 4 + 300)


def get_leagues(c):
    c.execute("SELECT DISTINCT group_id,twitter FROM wp_bp_twitter_teams")
    return c.fetchall()


def get_team_by_feedid(c, feedid):
    c.execute("SELECT t.group_id FROM wp_bp_teams t WHERE t.id = %d" % (feedid))
    return c.fetchone()


def get_players(c):
    c.execute("SELECT twitter,team_id FROM wp_bp_teams_players WHERE twitter IS NOT NULL")
    return c.fetchall()


def tweet_exists(tweet):
    c.execute("SELECT COUNT(id) FROM wp_bp_twitter WHERE content = '%s'" % conn.escape_string(
        tweet['user']['screen_name'] + ':' + tweet['text'].encode("iso-8859-1", "ignore").decode("utf-8", "ignore")))
    return c.fetchone()


def insert_twitt(c, data):
    if (data != ''):
        sql = "INSERT INTO wp_bp_twitter(secondary_item_id, user_id, component, type, action, content, primary_link, date_recorded, item_id, tweet_id, profile_picture ) VALUES %s " % data
        c.execute(sql)


# if 0:
#    print 0
if os.access(os.path.expanduser("~/.lockfile.twitter.lock"), os.F_OK):
    # if the lockfile is already there then check the PID number
    # in the lock file
    pidfile = open(os.path.expanduser("~/.lockfile.twitter.lock"), "r")
    pidfile.seek(0)
    old_pid = pidfile.readline()
    # Now we check the PID from lock file matches to the current
    # process PID
    if os.path.exists("/proc/%s" % old_pid):
        print "You already have an instance of the program running"
        print "It is running as process %s," % old_pid
        sys.exit(1)
    else:
        print "File is there but the program is not running"
        print "Removing lock file for the: %s as it can be there                 because of the program last time it was run" % old_pid
        os.remove(os.path.expanduser("~/.lockfile.twitter.lock"))
else:
    pidfile = open(os.path.expanduser("~/.lockfile.twitter.lock"), "w")
    pidfile.write("%s" % os.getpid())
    pidfile.close

    try:
        conn = MySQLdb.connect("", "", "", "")

        c = conn.cursor()

        insertdata = [];

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'Accept': 'text/html', 'User-Agent': user_agent}
        for league in get_leagues(c):
            league_name = league[1]
            print league_name
            try:
                # In the case of Women's NCAAB, the name changes
                if league_name.lower().replace(' ', '') == 'wncaab':
                    league_name = 'NCAAWomensBKB'
                url = 'http://api.twitter.com/1/statuses/user_timeline/' + league_name.lower().replace(' ',
                                                                                                       '') + '.json?count=10'
                req = urllib2.Request(url=url, headers=headers)
                res = urllib2.urlopen(req)
            except urllib2.HTTPError, e:
                print 'League HTTPError: '
                print e.code
            except urllib2.URLError, e:
                print 'League URLError: '
                print e.reason
            else:
                feed = res.read()

                decode_feed = simplejson.loads(feed)
                for tweet in decode_feed:
                    if tweet_exists(tweet)[0] == 0:
                        insertdata.append("('" + league_name.lower().replace(' ',
                                                                             '') + "',1,'groups','twitter_update','','" + conn.escape_string(
                            tweet['user']['screen_name'] + ':' + tweet['text'].encode("iso-8859-1", "ignore").decode(
                                "utf-8", "ignore")) + "','" + tweet['user']['screen_name'] + "','" + str(
                            get_twitter_date(tweet['created_at'])) + "'," + str(league[0]) + ",'" + tweet[
                                              'id_str'] + "','" + tweet['user']['profile_image_url'] + "')")
        data = str.join(',', insertdata)
        insert_twitt(c, data)

        conn.commit()
        c.close()
        conn.close()
        os.remove(os.path.expanduser("~/.lockfile.twitter.lock"))
        sys.exit(1)
    except MySQLdb.Error, e:
        print "Guru Meditation #%d: %s" % (e.args[0], e.args[1])
        conn.commit()
        c.close()
        conn.close()
        os.remove(os.path.expanduser("~/.lockfile.twitter.lock"))
        sys.exit(1)
