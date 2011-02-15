#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fearless'

import pycurl
import traceback
from statsdb import db_open, db_close, get_all_teams, insert_activity, get_parent
from statsutils import replace_nonascii, get_twitter_date2, debug, send_mail
import daemon
import json
import Queue
import threading

STREAM_URL = "https://stream.twitter.com/1/statuses/filter.json"
SEARCH_PATH = "track=%s"

queue = Queue.Queue()


def get_hashtags():
    cc = db_open()
    c = cc[0]
    conn = cc[1]
    hashtags = []
    for team in get_all_teams(c):
        tname = team[1]
        tcity = team[2]

        if tcity is not None and tcity != '' and tname is not None and tname != '':
            hashtags.append(
                str(tcity + tname).replace(" ", "").replace("'", "").replace("(", "").replace(")", "").replace("-",
                                                                                                               "").replace(
                    "&", "").replace(".", "").lower())

    hashtags = set(hashtags)

    db_close(c, conn)
    return hashtags


def get_hashtags2():
    cc = db_open()
    c = cc[0]
    conn = cc[1]
    hashtags = []
    for team in get_all_teams(c):
        item_id = team[0]
        tname = team[1]
        tcity = team[2]
        gslug = team[4]
        gparent = team[5]
        gname = team[6]

        if tcity is not None and tcity != '' and tname is not None and tname != '':
            tag = str(tcity + tname).replace(" ", "").replace("'", "").replace("(", "").replace(")", "").replace("-",
                                                                                                                 "").replace(
                "&", "").replace(".", "").lower()
            hashtags.append([tag, item_id, gslug, gparent, gname])

    db_close(c, conn)
    return hashtags


class ThreadTwitter(threading.Thread):
    def __init__(self, queue, user, password, hashtags, hashtags2):
        threading.Thread.__init__(self)
        self.queue = queue
        self.user = user
        self.password = password
        self.hashtags2 = hashtags2
        self.hashtags = hashtags

    def do_tweet(self, data):
        cc2 = db_open()
        c2 = cc2[0]
        conn2 = cc2[1]
        try:
            tweet = json.loads(data)
            print tweet['text']
            print tweet['created_at']
            print get_twitter_date2(tweet['created_at'])
            for hashtag in self.hashtags2:
                item_id = hashtag[1]
                tag = str(hashtag[0])
                gname = str(hashtag[4])
                gslug = str(hashtag[2])
                gparent = int(hashtag[3])
                parent = get_parent(c2, gparent)
                if replace_nonascii(tweet['text'].encode("latin-1", "ignore").decode("latin-1", "ignore")).lower().find(
                        '#' + tag) > -1:
                    sql = "(10000000,'groups','twitter_update','" + replace_nonascii(tweet['user'][
                                                                                         'screen_name'] + " posted an update in the team <a href=\"" +
                                                                                     parent[
                                                                                         0] + "/" + gslug + "/\">" + gname + "</a>:") + "','" + replace_nonascii(
                        tweet['text'].encode("latin-1", "ignore").decode("latin-1", "ignore")) + "','" + tweet['user'][
                              'screen_name'] + "','" + str(get_twitter_date2(tweet['created_at'])) + "','" + str(
                        item_id) + "','" + tweet['id_str'] + "','" + tweet['user']['profile_image_url'] + "')"
                    insert_activity(c2, sql)
                    conn2.commit()
                    break
            db_close(c2, conn2)
        except:
            db_close(c2, conn2)
            print traceback.format_exc()
            return

    def run(self):
        hashtags = str.join(',', self.hashtags)
        conn = pycurl.Curl()
        conn.setopt(pycurl.POST, 1)
        conn.setopt(pycurl.POSTFIELDS, SEARCH_PATH % hashtags)
        conn.setopt(pycurl.HTTPHEADER, ["Connection: keep-alive", "Keep-Alive: 84600"])
        conn.setopt(pycurl.USERPWD, "%s:%s" % (self.user, self.password))
        conn.setopt(pycurl.URL, STREAM_URL)
        conn.setopt(pycurl.WRITEFUNCTION, self.do_tweet)
        conn.perform()
        # signals to queue job is done
        self.queue.task_done()


if __name__ == "__main__":
    with daemon.DaemonContext():
        try:
            hashtags2 = get_hashtags2()
            hashtags = list(get_hashtags())
            list_of_groups = zip(*(iter(hashtags),) * 400)
            t = ThreadTwitter(queue, '', '', list_of_groups[0], hashtags2)
            #            t.setDaemon(True)
            t.start()
            t = ThreadTwitter(queue, '', '', list_of_groups[1], hashtags2)
            #            t.setDaemon(True)
            t.start()
            t = ThreadTwitter(queue, '', '', list_of_groups[2], hashtags2)
            #            t.setDaemon(True)
            t.start()
            t = ThreadTwitter(queue, '', '', list_of_groups[3], hashtags2)
            #            t.setDaemon(True)
            t.start()
            queue.join()
        except:
            if debug:
                print traceback.format_exc()
            else:
                send_mail("trackbyhash", traceback.format_exc())
