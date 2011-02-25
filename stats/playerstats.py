#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from statsfiles import playerstats_files
from statsutils import find_value_in_array4args, send_mail, debug, replace_nonascii
from statsdb import db_open, db_close, get_stats, insert_stats

__author__ = 'fearless'


class NBAHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.player_global_id = 0
        self.group = ''
        self.type = ''
        self.num = ''
        self.season = ''
        self.split = 'total'
        self.insertdata = []
        self.stats = []

        self.isSeason = False
        self.isPlayerSplits = False
        self.isPlayerSplit = False

        self.splitsName = ['nba-player-splits', 'cbk-player-stats', 'nhl-player-splits', 'soccer-ifb-player-stats',
                           'wcbk-player-stats']
        self.splitName = ['cfb-player-stats-passing', 'cfb-player-stats-overall', 'cfb-player-stats-rushing',
                          'cfb-player-stats-defense', 'cfb-player-stats-receiving',
                          'cfb-player-stats-kickoff-returning', 'cfb-player-stats-kicking',
                          'cfb-player-stats-punt-returning', 'cfb-player-stats-punting', 'baseball-mlb-stats-hitting',
                          'baseball-mlb-stats-defense', 'baseball-mlb-stats-pitching', 'nhl-player-split-skater',
                          'nhl-player-split-goalie', 'nfl-player-stats-overall', 'nfl-player-stats-defense',
                          'nfl-player-stats-miscellaneous', 'nfl-player-stats-kickoff-returning',
                          'nfl-player-stats-punt-returning', 'nfl-player-stats-rushing', 'nfl-player-stats-receiving',
                          'nfl-player-stats-passing', 'nfl-player-stats-kicking', 'nfl-player-stats-punting']
        self.splitNameOther = ['nba-player-split', 'cbk-player-stat', 'nhl-player-split', 'ifb-regular-stats',
                               'wcbk-player-stat']
        self.NotIn = [
            'spanish-name',
            'team-info',
            'team-name',
            'team-city',
            'team-code',
            'team-conference',
            'team-games',
            'conf',
            'conference',
            'name',
            'player-name',
            'has-stats',
            'player-position',
            'player-number',
            'year',
            'college-name',
            'college-code',
        ]

    def startElement(self, name, attrs):
        if name in ['sports-rankings', 'sports-player-stats']:
            self.insertdata = []
        elif name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            if self.season is None:
                self.season = attrs.get('year')
        elif name in self.splitsName:
            self.isPlayerSplits = True
        elif name in self.splitNameOther:
            self.isPlayerSplit = True
            self.split = str(attrs.get('type'))
        elif name in self.splitName:
            self.isPlayerSplit = True
            self.split = name
        elif name == 'player-code':
            self.player_global_id = attrs.get('global-id')
            self.stats = get_stats(c, self.player_global_id, self.season)
        elif name not in self.NotIn and name not in self.splitName and self.isPlayerSplit:
            self.group = name
            for attrName in attrs.keys():
                self.type = attrName
                self.num = attrs.get(attrName)
                if self.num == 'false' or self.num == '-':
                    self.num = 0
                elif self.num == 'true':
                    self.num = 1
                self.id = int(find_value_in_array4args(self.stats, self.group, self.type, self.split) or 0)
                # print self.group
                # print self.num
                # print self.type
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.player_global_id) +
                                       "','"
                                       + str(self.season) +
                                       "','"
                                       + self.split +
                                       "')")
        return

    def endElement(self, name):
        if name in ['sports-rankings', 'sports-player-stats']:
            data = str.join(',', self.insertdata)
            insert_stats(c, data)
        elif name == 'season':
            self.isSeason = False
        elif name in self.splitsName:
            self.isPlayerSplits = False
        elif name in self.splitNameOther and name in self.splitName:
            self.isPlayerSplit = False


if __name__ == "__main__":
    if os.access(os.path.expanduser("~/.lockfile.playerstats.lock"), os.F_OK):
        # if the lockfile is already there then check the PID number
        # in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.playerstats.lock"), "r")
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
            os.remove(os.path.expanduser("~/.lockfile.playerstats.lock"))
    else:
        pidfile = open(os.path.expanduser("~/.lockfile.playerstats.lock"), "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close

        try:
            cc = db_open()
            c = cc[0]
            conn = cc[1]

            parser = make_parser()
            for file in playerstats_files:
                if not debug:
                    print file
                curHandler = NBAHandler()
                parser.setContentHandler(curHandler)
                parser.parse(open(file))

            db_close(c, conn)
            os.remove(os.path.expanduser("~/.lockfile.playerstats.lock"))
        except:
            if debug:
                print traceback.format_exc()
            else:
                send_mail("playerstats", traceback.format_exc())
            os.remove(os.path.expanduser("~/.lockfile.playerstats.lock"))
            sys.exit(1)
