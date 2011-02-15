#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from statsdb import db_open, db_close, tweet_exists, insert_twitt, get_all_teams
from statsutils import replace_nonascii, get_twitter_date

__author__ = 'fearless'

import httplib
import json
import logging
import socket
import time
import urllib

SEARCH_HOST = "search.twitter.com"
SEARCH_PATH = "/search.json"


class TagCrawler(object):
    ''' Crawl twitter search API for matches to specified tag.  Use since_id to
    hopefully not submit the same message twice.  However, bug reports indicate
    since_id is not always reliable, and so we probably want to de-dup ourselves
    at some level '''

    def __init__(self, max_id, tag, interval):
        self.max_id = max_id
        self.tag = tag
        self.interval = interval

    def search(self):
        c = httplib.HTTPConnection(SEARCH_HOST)
        params = {'q': self.tag}
        if self.max_id is not None:
            params['since_id'] = self.max_id
        path = "%s?%s" % (SEARCH_PATH, urllib.urlencode(params))
        try:
            c.request('GET', path)
            r = c.getresponse()
            data = r.read()
            c.close()
            try:
                result = json.loads(data)
            except ValueError:
                return None
            if 'results' not in result:
                return None
            self.max_id = result['max_id']
            return result['results']
        except (httplib.HTTPException, socket.error, socket.timeout), e:
            logging.error("search() error: %s" % (e))
            return None

    def loop(self):
        while True:
            logging.info("Starting search")
            data = self.search()
            if data:
                logging.info("%d new result(s)" % (len(data)))
                self.submit(data)
            else:
                logging.info("No new results")
            logging.info("Search complete sleeping for %d seconds"
                         % (self.interval))
            time.sleep(float(self.interval))

    def submit(self, data):
        print data
        pass


if __name__ == "__main__":
    if os.access(os.path.expanduser("~/.lockfile.twittertags.lock"), os.F_OK):
        # if the lockfile is already there then check the PID number
        # in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.twittertags.lock"), "r")
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
            os.remove(os.path.expanduser("~/.lockfile.twittertags.lock"))
    else:
        pidfile = open(os.path.expanduser("~/.lockfile.twittertags.lock"), "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close
        cc = db_open()
        c = cc[0]
        conn = cc[1]
        for team in get_all_teams(c):

            item_id = team[0]
            tname = team[1]
            tcity = team[2]
            talias = team[3]

            hashtags = []
            #            if tname is not None and tname != '':
            #                hashtags.append(str(tname).replace(" ", "").replace("'", "").lower())
            if tcity is not None and tcity != '' and tname is not None and tname != '':
                hashtags.append(
                    str(tcity + tname).replace(" ", "").replace("'", "").replace("(", "").replace(")", "").replace("-",
                                                                                                                   "").replace(
                        "&", "").replace(".", "").lower())
            #            if tcity is not None and tcity != '' and tname is not None and tname != '':
            #                hashtags.append(str(tcity+tname).replace(" ", "").replace("'", ""))
            #
            #            if talias is not None and talias != '':
            #                hashtags.append(str(talias).replace(" ", "").lower())

            #        activities = get_activities(c, item_id)
            #        for activity in activities:
            #            extract_hash_tags(activity[1],hashtags)

            #        hashtags = [ item for innerlist in hashtags for item in innerlist ]
            #        hashtags = set(hashtags)
            print hashtags
            for tag in hashtags:
                tagCrawler = TagCrawler(max_id=0, tag="#" + tag, interval=10)
                tweets = tagCrawler.search()
                if tweets is not None:
                    # decode_feed = simplejson.loads(tweets)
                    insertdata = []
                    for tweet in tweets:
                        if tweet_exists(c, tweet)[0] == 0:
                            insertdata.append("(1,'groups','twitter_update','','" + replace_nonascii(
                                tweet['from_user'] + ":" + tweet['text'].encode("latin-1", "ignore").decode("latin-1",
                                                                                                            "ignore")) + "','" +
                                              tweet['from_user'] + "','" + str(
                                get_twitter_date(tweet['created_at'])) + "','" + str(item_id) + "','" + tweet[
                                                  'id_str'] + "','" + tweet['profile_image_url'] + "')")
                    data = str.join(',', insertdata)
                    insert_twitt(c, data)
                    conn.commit()

        db_close(c, conn)
        os.remove(os.path.expanduser("~/.lockfile.twittertags.lock"))
