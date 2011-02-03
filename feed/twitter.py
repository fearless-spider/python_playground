import MySQLdb
# from urllib2 import HTTPError, urlopen, URLError
import urllib2
import simplejson
import time
import feedparser
import re
from datetime import datetime
import os.path
import sys


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
    time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")
    return datetime.fromtimestamp(time.mktime(time_struct))


def get_leagues(c):
    c.execute("SELECT group_id,group_id,twitter FROM wp_bp_twitter_teams")
    # c.execute("SELECT * FROM wp_bp_groups WHERE type='league'")
    return c.fetchall()


def get_team_by_feedid(c, feedid):
    c.execute(
        "SELECT g.id FROM wp_bp_groups g LEFT JOIN wp_bp_teams t ON g.xmlurl = t.feed_id WHERE t.id = %d" % (feedid))
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
        sql = "INSERT INTO wp_bp_twitter( user_id, component, type, action, content, primary_link, date_recorded, item_id ) VALUES %s " % data
        c.execute(sql)


def insert_twitts(c):
    twitter = os.path.join(os.path.dirname(__file__), 'twitter.txt')
    print twitter
    sql = "LOAD DATA LOCAL INFILE '" + conn.escape_string(
        twitter) + "' INTO TABLE wp_bp_twitter FIELDS TERMINATED BY ',' enclosed by '|' LINES TERMINATED BY '\r\n' (user_id, component, type, action, content, primary_link, date_recorded, item_id);"
    c.execute(sql)


# fileHandle = open( 'twitter.txt', 'w')

try:
    conn = MySQLdb.connect("localhost", "", "", "")

    c = conn.cursor()

    insertdata = []

    for league in get_leagues(c):
        league_name = league[2]
        print league_name
        try:
            # In the case of Women's NCAAB, the name changes
            if league_name.lower().replace(' ', '') == 'wncaab':
                league_name = 'NCAAWomensBKB'
            url = 'http://api.twitter.com/1/statuses/user_timeline/' + league_name.lower().replace(' ',
                                                                                                   '') + '.json?count=10'
            #        url1 = 'http://twitter.com/'+league_name.lower().replace(' ','')+'/'
            #        twits = get_twitter(url1)
            #        print url
            res = urllib2.urlopen(url)
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
                    insertdata.append("(1,'groups','twitter_update','','" + conn.escape_string(
                        tweet['user']['screen_name'] + ':' + tweet['text'].encode("iso-8859-1", "ignore").decode(
                            "utf-8", "ignore")) + "','','" + str(get_twitter_date(tweet['created_at'])) + "'," + str(
                        league[0]) + ")")
    #                fileHandle.write('|1|,|groups|,|twitter_update|,||,|' + conn.escape_string(tweet['user']['screen_name']+':'+tweet['text'].encode("iso-8859-1","ignore").decode("utf-8","ignore")) + '|,||,|' + str(get_twitter_date(tweet['created_at'])) + '|,|' + str(league[0]) + '|\n')
    #                insert_twitt(c,league,tweet)

    # import sys
    # sys.exit('fin league')
    headers = {'Accept': 'text/html'}
    for player in get_players(c):
        league_name = player[0]
        team = get_team_by_feedid(c, player[1])
        print league_name
        try:
            url = 'https://api.twitter.com/1/statuses/user_timeline/' + league_name + '.json?count=10'
            req = urllib2.Request(url=url, headers=headers)
            res = urllib2.urlopen(req)
        # res = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            print 'Player HTTPError: '
            print e.code
        except urllib2.URLError, e:
            print 'Player URLError:'
            print e.reason
        else:
            feed = res.read()

            decode_feed = simplejson.loads(feed)
            for tweet in decode_feed:
                if tweet_exists(tweet)[0] == 0 and tweet['user']['screen_name'] == league_name:
                    insertdata.append("(1,'groups','twitter_update','','" + conn.escape_string(
                        tweet['user']['screen_name'] + ':' + tweet['text'].encode("iso-8859-1", "ignore").decode(
                            "utf-8", "ignore")) + "','','" + str(get_twitter_date(tweet['created_at'])) + "'," + str(
                        team[0]) + ")")
    #                fileHandle.write('|1|,|groups|,|twitter_update|,||,|' + conn.escape_string(tweet['user']['screen_name']+':'+tweet['text'].encode("iso-8859-1","ignore").decode("utf-8","ignore")) + '|,||,|' + str(get_twitter_date(tweet['created_at'])) + '|,|' + str(team[0]) + '|\n')
    #                insert_twitt(c,team,tweet)
    # fileHandle.close()
    data = str.join(',', insertdata)
    insert_twitt(c, data)

    conn.commit()
    c.close()
    conn.close()
except MySQLdb.Error, e:
    print "Guru Meditation #%d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
