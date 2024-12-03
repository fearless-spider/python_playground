#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pycurl
import traceback
from statsdb import db_open, db_close, get_all_teams, get_twitters, get_parent, insert_activity, activity_exists
from statsutils import replace_nonascii

__author__ = 'fearless'

cc = db_open()
c = cc[0]
conn = cc[1]


def get_hashtags2():
    hashtags = []
    for team in get_all_teams(c):
        item_id = team[0]
        tname = team[1]
        tcity = team[2]
        gslug = team[4]
        gparent = team[5]
        gname = team[6]

        if tname is not None and tname != '':
            tag = [str(tname).replace(" ", "").replace("'", "").lower(), item_id]
            hashtags.append([tag, item_id, gslug, gparent, gname])
        if tcity is not None and tcity != '' and tname is not None and tname != '':
            tag = str(tcity + tname).replace(" ", "").replace("'", "").replace("(", "").replace(")", "").replace("-",
                                                                                                                 "").replace(
                "&", "").lower()
            hashtags.append([tag, item_id, gslug, gparent, gname])

    return hashtags


if __name__ == "__main__":
    hashtags2 = get_hashtags2()
    for hashtag in hashtags2:
        item_id = hashtag[1]
        tag = str(hashtag[0])
        gname = str(hashtag[4])
        gslug = str(hashtag[2])
        gparent = int(hashtag[3])
        parent = get_parent(c, gparent)

        twitts = get_twitters(c, item_id)
        for twitt in twitts:
            if twitt[3].lower().find('#' + tag) > -1 and twitt[0] == 'groups' and twitt[1] == 'twitter_update' and \
                    activity_exists(c, twitt[7])[0] == 0:
                print parent
                sql = "(10000000,'groups','twitter_update','" + replace_nonascii(
                    twitt[4] + " posted an update in the team <a href=\"/groups/" + parent[
                        0] + "/" + gslug + "/\">" + gname + "</a>:") + "','" + replace_nonascii(twitt[3]) + "','" + \
                      twitt[4] + "','" + str(twitt[5]) + "','" + str(item_id) + "','" + str(
                    twitt[7] or '') + "','" + str(twitt[8] or '') + "')"
                insert_activity(c, sql)
                conn.commit()
    db_close(c, conn)
