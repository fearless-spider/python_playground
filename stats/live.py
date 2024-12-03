#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from statsfiles import live_files
from statsutils import find_value_in_array2args, path, debug, send_mail
from statsdb import get_teams, db_open, db_close, get_score, insert_boxscores, insert_records, get_records

__author__ = 'fearless'


class LIVEHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.league_id = league_id
        self.date = ''
        self.time = ''
        self.status = ''
        self.home_team_short = ''
        self.home_team_id = 0
        self.home_score = 0
        self.away_team_short = ''
        self.away_team_id = 0
        self.away_score = 0
        self.competition_id = ''
        self.period = ''
        self.period_time = ''
        self.insertdata = []
        self.teams = []

        self.isSeason = False
        self.isNBAScores = False
        self.isNBAScore = False
        self.isHome = False
        self.isAway = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            if self.season is None:
                self.season = attrs.get('year')
            self.teams = get_teams(c, league_name)
        elif name in ['baseball-mlb-scores', 'wnba-scores', 'wcbk-scores', 'nba-scores', 'cbk-scores', 'cfb-scores',
                      'nfl-scores', 'nhl-scores', 'soccer-ifb-scores']:
            self.isNBAScores = True
            self.insertdata = []
        elif name in ['baseball-mlb-score', 'wnba-score', 'wcbk-score', 'nba-score', 'cbk-score', 'cfb-score',
                      'nfl-score', 'nhl-score', 'ifb-score']:
            self.isNBAScore = True
            self.id = 0
            self.date = ''
            self.time = ''
            self.status = ''
            self.home_team_short = ''
            self.home_team_global_id = ''
            self.home_team_id = 0
            self.home_score = 0
            self.away_team_short = ''
            self.away_team_global_id = ''
            self.away_team_id = 0
            self.away_score = 0
            self.competition_id = ''
            self.period = ''
            self.period_time = ''
            self.away_wins = ''
            self.away_losses = ''
            self.away_pct = ''
            self.home_wins = ''
            self.home_losses = ''
            self.home_pct = ''
        elif name == 'visiting-team':
            self.isAway = True
        elif name == 'home-team':
            self.isHome = True
        elif name == 'gamestate':
            self.status = attrs.get('status')
            quarter = attrs.get('quarter')
            if quarter is None:
                quarter = attrs.get('half')
            if quarter is None:
                quarter = attrs.get('period')
            if quarter is None:
                quarter = ''
            if quarter == '1':
                self.period = (quarter + 'st')
            if quarter == '2':
                self.period = (quarter + 'nd')
            if quarter == '3':
                self.period = (quarter + 'rd')
            if quarter > '3':
                self.period = (quarter + 'th')
            if attrs.get('minutes') is not None and attrs.get('seconds') is not None:
                seconds = attrs.get('seconds')
                if attrs.get('seconds') == '':
                    seconds = '00'
                self.period_time = attrs.get('minutes') + ':' + seconds
            if self.period_time == ':':
                self.period_time = '00:00'
            if self.period == '':
                self.period = attrs.get('inning')
                if self.period is None:
                    self.period = ''
        elif name == 'gamecode':
            self.competition_id = attrs.get('global-id')
            if self.competition_id is None:
                self.competition_id = attrs.get('global-code')
        elif name == 'date':
            self.date = attrs.get('year') + '-' + attrs.get('month') + '-' + attrs.get('date')
        elif name == 'time':
            self.time = attrs.get('hour') + ':' + attrs.get('minute') + ':00'
        elif name == 'team-code':
            if self.isAway:
                self.away_team_global_id = attrs.get('global-id')
                self.away_team_id = find_value_in_array2args(self.teams, attrs.get('global-id'))
            else:
                self.home_team_global_id = attrs.get('global-id')
                self.home_team_id = find_value_in_array2args(self.teams, attrs.get('global-id'))
        elif name == 'team-name':
            if self.isAway:
                self.away_team_short = attrs.get('alias')
            else:
                self.home_team_short = attrs.get('alias')
        elif name == 'team-info':
            if self.isAway:
                self.away_team_global_id = attrs.get('global-id')
                self.away_team_id = find_value_in_array2args(self.teams, attrs.get('global-id'))
                self.away_team_short = attrs.get('alias')
            else:
                self.home_team_global_id = attrs.get('global-id')
                self.home_team_id = find_value_in_array2args(self.teams, attrs.get('global-id'))
                self.home_team_short = attrs.get('alias')
        elif name == 'linescore':
            score = attrs.get('score')
            if self.isAway:
                self.away_score = score
                if self.away_score == '':
                    self.away_score = 0
            else:
                self.home_score = score
                if self.home_score == '':
                    self.home_score = 0
        elif name == 'record':
            wins = attrs.get('wins')
            if self.isAway:
                self.away_wins = wins
                if self.away_wins == '':
                    self.away_wins = 0
            else:
                self.home_wins = wins
                if self.home_wins == '':
                    self.home_wins = 0

            losses = attrs.get('losses')
            if self.isAway:
                self.away_losses = losses
                if self.away_losses == '':
                    self.away_losses = 0
            else:
                self.home_losses = losses
                if self.home_losses == '':
                    self.home_losses = 0

            pct = attrs.get('pct')
            if self.isAway:
                self.away_pct = pct
                if self.away_pct == '':
                    self.away_pct = 0
            else:
                self.home_pct = pct
                if self.home_pct == '':
                    self.home_pct = 0

        elif name == 'home-score' and attrs.get('type') == 'runs':
            self.home_score = attrs.get('number')
            if self.home_score == '':
                self.home_score = 0
        elif name == 'visiting-score' and attrs.get('type') == 'runs':
            self.away_score = attrs.get('number')
            if self.away_score == '':
                self.away_score = 0
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name in ['baseball-mlb-scores', 'wnba-scores', 'wcbk-scores', 'nba-scores', 'cbk-scores', 'cfb-scores',
                      'nfl-scores', 'nhl-scores', 'soccer-ifb-scores']:
            self.isNBAScores = False
            data = str.join(',', self.insertdata)
            # print data
            insert_boxscores(c, data)
        elif name == 'visiting-team':
            self.isAway = False
        elif name == 'home-team':
            self.isHome = False
        elif name == 'record':
            if self.isAway:
                cid = get_records(c, self.competition_id, self.away_team_global_id)
                sql = "('" + self.competition_id + "','" + str(self.away_wins) + "','" + str(
                    self.away_losses) + "','" + str(self.away_pct) + "','" + str(self.away_team_global_id) + "')"
                if cid is None:
                    insert_records(c, sql)
            else:
                cid = get_records(c, self.competition_id, self.home_team_global_id)
                sql = "('" + self.competition_id + "','" + str(self.home_wins) + "','" + str(
                    self.home_losses) + "','" + str(self.home_pct) + "','" + str(self.home_team_global_id) + "')"
                if cid is None:
                    insert_records(c, sql)
        elif name in ['baseball-mlb-score', 'wnba-score', 'wcbk-score', 'nba-score', 'cbk-score', 'cfb-score',
                      'nfl-score', 'nhl-score', 'ifb-score']:
            self.isNBAScore = False
            cid = get_score(c, self.competition_id)
            if cid is not None:
                self.id = int(cid[0] or 0)
            else:
                self.id = 0
            self.insertdata.append("("
                                   + str(self.id) +
                                   ","
                                   + str(self.league_id) +
                                   ",'"
                                   + str(self.date + ' ' + self.time) +
                                   "','"
                                   + str(self.status) +
                                   "','"
                                   + str(self.home_team_short) +
                                   "',"
                                   + str(self.home_team_id) +
                                   ","
                                   + str(self.home_score) +
                                   ",'"
                                   + str(self.away_team_short) +
                                   "',"
                                   + str(self.away_team_id) +
                                   ","
                                   + str(self.away_score) +
                                   ",'"
                                   + str(self.competition_id) +
                                   "','"
                                   + str(self.period) +
                                   "','"
                                   + str(self.period_time) +
                                   "')")


if __name__ == "__main__":
    if os.access(os.path.expanduser("~/.lockfile.live.lock"), os.F_OK):
        # if the lockfile is already there then check the PID number
        # in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.live.lock"), "r")
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
            os.remove(os.path.expanduser("~/.lockfile.live.lock"))
    else:
        pidfile = open(os.path.expanduser("~/.lockfile.live.lock"), "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close()

        try:
            cc = db_open()
            c = cc[0]
            conn = cc[1]
            parser = make_parser()
            for file in live_files:
                if os.path.exists(path + file[1]):
                    if debug:
                        print file[1]
                    league_id = file[0]
                    league_name = file[2]
                    curHandler = LIVEHandler()
                    parser.setContentHandler(curHandler)
                    parser.parse(open(path + file[1]))

            db_close(c, conn)
            os.remove(os.path.expanduser("~/.lockfile.live.lock"))
        except:
            if debug:
                print traceback.format_exc()
            else:
                send_mail(__file__, traceback.format_exc())
            os.remove(os.path.expanduser("~/.lockfile.live.lock"))
            sys.exit(1)
