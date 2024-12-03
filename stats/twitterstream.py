#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pycurl
import traceback
from statsdb import db_open, db_close, get_twitter_teams, insert_twitt
from statsutils import replace_nonascii, get_twitter_date2, debug, send_mail
import daemon
import json
import Queue
import threading

__author__ = 'bespider'

STREAM_URL = "https://stream.twitter.com/1/statuses/filter.json"
SEARCH_PATH = "follow=%s"

queue = Queue.Queue()


class ThreadTwitter(threading.Thread):
    def __init__(self, queue, user, password, ids):
        threading.Thread.__init__(self)
        self.queue = queue
        self.user = user
        self.password = password
        self.ids = ids

    def do_tweet(self, data):
        print "do tweet"
        cc2 = db_open()
        c2 = cc2[0]
        conn2 = cc2[1]
        try:
            tweet = json.loads(data)
            print tweet
            for id in self.ids:
                #                print tweet['in_reply_to_user_id_str'] == id[0]
                print tweet['user']['id_str'] == id[0]
                item_id = id[1]
                if tweet['user']['id_str'] == id[0]:  # or tweet['in_reply_to_user_id_str'] == id[0]:
                    sql = "(" + str(item_id) + ",'groups','twitter_update','" + replace_nonascii(
                        tweet['user']['screen_name']) + ":" + replace_nonascii(
                        tweet['text'].encode("latin-1", "ignore").decode("latin-1", "ignore")) + "','','" + \
                          tweet['user']['screen_name'] + "','" + str(
                        get_twitter_date2(tweet['created_at'])) + "','" + str(item_id) + "','" + tweet[
                              'id_str'] + "','" + tweet['user']['profile_image_url'] + "')"
                    print sql
                    insert_twitt(c2, sql)
                    conn2.commit()
                    break
            db_close(c2, conn2)
        except:
            db_close(c2, conn2)
            print traceback.format_exc()
            return

    def run(self):
        ids2 = []
        for id in self.ids:
            ids2.append(id[0])
        ids = str.join(',', ids2)
        conn = pycurl.Curl()
        conn.setopt(pycurl.POST, 1)
        conn.setopt(pycurl.POSTFIELDS, SEARCH_PATH % ids)
        conn.setopt(pycurl.HTTPHEADER, ["Connection: keep-alive", "Keep-Alive: 84600"])
        conn.setopt(pycurl.USERPWD, "%s:%s" % (self.user, self.password))
        conn.setopt(pycurl.URL, STREAM_URL)
        conn.setopt(pycurl.WRITEFUNCTION, self.do_tweet)
        conn.perform()
        # signals to queue job is done
        self.queue.task_done()


if __name__ == "__main__":

    with daemon.DaemonContext():
        #    if 1:
        try:
            cc = db_open()
            c = cc[0]
            conn = cc[1]
            ids = get_twitter_teams(c)
            db_close(c, conn)
            t = ThreadTwitter(queue, '', '', ids)
            t.start()
            queue.join()
        except:
            if debug:
                print traceback.format_exc()
            else:
                send_mail("twitterstream", traceback.format_exc())
