#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from statsfiles import leaders_files
from statsutils import find_value_in_array2args, replace_nonascii, send_mail, debug, path
from statsdb import db_open, db_close, get_leaders, insert_leaders

__author__ = 'fearless'


class NBAHandler(ContentHandler):
    def __init__(self):
        self.leadersTag = ['baseball-mlb-leaders', 'wnba-leaders', 'wcbk-leaders', 'nba-leaders', 'cbk-leaders',
                           'nhl-leaders', 'soccer-ifb-leaders', 'cfb-leaders', 'football-nfl-leaders']

        self.id = 0
        self.global_id = 0
        self.category = ''
        self.category_heading = ''
        self.firstname = ''
        self.lastname = ''
        self.alias = ''
        self.ranking = 0
        self.stat = 0.0
        self.tie = 0
        self.season = ''
        self.league = ''
        self.conference = ''
        self.insertdata = []
        self.leaders = []

        self.isSeason = False
        self.isLeaders = False
        self.isCategory = False
        self.isRanking = 0

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            if self.season is None:
                self.season = attrs.get('year')
        elif name in self.leadersTag:
            self.isLeaders = True
            self.insertdata = []
        elif name == 'category':
            self.isCategory = True
            self.category = attrs.get('category')
            if self.category is None:
                self.category = ''
            else:
                self.category = replace_nonascii(self.category)
            self.category_heading = attrs.get('category_heading')
            if self.category_heading is None:
                self.category_heading = replace_nonascii(attrs.get('category-heading'))
            self.conference = attrs.get('conference')
            if self.conference is None:
                self.conference = ''
            else:
                self.conference = self.conference
            if self.conference == '':
                self.conference = attrs.get('league')
            if self.conference is None:
                self.conference = ''
            else:
                self.conference = replace_nonascii(self.conference)

            self.league = league_name
            self.leaders = get_leaders(c, self.season, self.league, self.category, self.conference)
        elif name == 'ranking':
            if attrs.has_key('ranking'):
                self.isRanking = 2
                self.ranking = attrs.get('ranking')
                self.tie = attrs.get('tie')
                if self.tie is None:
                    self.tie = attrs.get('tied')
                if self.tie == 'false':
                    self.tie = 0
                else:
                    self.tie = 1
            else:
                self.isRanking = 1
        elif name == 'name':
            self.firstname = replace_nonascii(attrs.get('first-name'))
            self.lastname = replace_nonascii(attrs.get('last-name'))
        elif name == 'player-id' or name == 'player-code':
            self.global_id = attrs.get('global-id')
        elif name == 'team-name':
            self.alias = attrs.get('alias')
            if self.alias is not None:
                self.alias = replace_nonascii(self.alias)
            else:
                self.alias = replace_nonascii(attrs.get('name'))
        elif name == 'team-info':
            self.alias = replace_nonascii(attrs.get('alias'))
        elif name == 'stat':
            self.stat = attrs.get('stat')
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name in self.leadersTag:
            self.isLeaders = False
            data = str.join(',', self.insertdata)
            insert_leaders(c, data)
        elif name == 'category':
            self.isCategory = False
            self.category = ''
            self.conference = ''
            self.category_heading = ''
            self.league = ''
        elif name == 'ranking' and self.isRanking == 2:
            self.isRanking = 1
        elif name == 'ranking' and self.isRanking == 1:
            self.isRanking = 0
            self.id = find_value_in_array2args(self.leaders, self.global_id)
            if self.id is None:
                self.id = 0

            self.insertdata.append("("
                                   + str(self.id) +
                                   ",'"
                                   + str(self.global_id) +
                                   "','"
                                   + self.category +
                                   "','"
                                   + self.category_heading +
                                   "','"
                                   + self.firstname +
                                   "','"
                                   + self.lastname +
                                   "','"
                                   + self.alias +
                                   "',"
                                   + str(self.ranking) +
                                   ",'"
                                   + self.stat +
                                   "',"
                                   + str(self.tie) +
                                   ",'"
                                   + self.season +
                                   "','"
                                   + self.league +
                                   "','"
                                   + self.conference +
                                   "')")


if __name__ == "__main__":
    if os.access(os.path.expanduser("~/.lockfile.leaders.lock"), os.F_OK):
        # if the lockfile is already there then check the PID number
        # in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.leaders.lock"), "r")
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
            os.remove(os.path.expanduser("~/.lockfile.leaders.lock"))
    else:
        pidfile = open(os.path.expanduser("~/.lockfile.leaders.lock"), "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close

        try:
            cc = db_open()
            c = cc[0]
            conn = cc[1]
            parser = make_parser()
            for file in leaders_files:
                league_name = file[0]
                if debug:
                    print file[1]
                if os.path.exists(path + file[1]):
                    curHandler = NBAHandler()
                    parser.setContentHandler(curHandler)
                    parser.parse(open(path + file[1]))

            db_close(c, conn)
            os.remove(os.path.expanduser("~/.lockfile.leaders.lock"))
        except:
            if debug:
                print traceback.format_exc()
            else:
                send_mail(traceback.format_exc())
            os.remove(os.path.expanduser("~/.lockfile.leaders.lock"))
            sys.exit(1)
