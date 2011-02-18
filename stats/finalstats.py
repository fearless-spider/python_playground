#! /usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import sys
import re
from statsfiles import finalstats_files
from statsutils import find_value_in_array2args, replace_nonascii, path, debug, send_mail
from statsdb import db_open, db_close, get_teams, get_score, get_finalstats, insert_playerstats, insert_teamstats, \
    insert_scores, insert_linescores, insert_boxscores, insert_competitions


class Stats():
    stat_type = ''
    stat = ''
    value = ''


class NBAHandler(ContentHandler):
    def __init__(self):
        self.boxscore = ['nba-boxscore', 'cbk-boxscore', 'wcbk-boxscore', 'nhl-boxscore', 'nfl-boxscore',
                         'baseball-mlb-boxscore', 'wnba-boxscore', 'ifb-boxscore']
        self.id = 0
        self.player_global_id = ''
        self.team_global_id = ''
        self.stat_type = ''
        self.stat = ''
        self.value = ''
        self.season = ''
        self.home = 't'
        self.quarter = ''
        self.score = ''
        self.num1 = ''
        self.num2 = ''
        self.gamecode = ''
        self.gametype = ''
        self.stadium_name = ''
        self.stadium_city = ''
        self.stadium_state = ''
        self.stadium_country = ''
        self.date = ''
        self.gamestate = ''
        self.away_team_name = ''
        self.away_team_city = ''
        self.away_team_alias = ''
        self.away_team_global_id = ''
        self.away_team_score = ''
        self.home_team_name = ''
        self.home_team_city = ''
        self.home_team_alias = ''
        self.home_team_global_id = ''
        self.home_team_score = ''
        self.split = ''
        self.teams = []
        self.competitions = []
        self.linescores = []
        self.teamstats = []
        self.playerstats = []
        self.insertdata = []
        self.playerstat = []
        self.scores = []

        self.isBoxScore = False
        self.isHome = False
        self.isAway = False
        self.isTeam = False
        self.isPlayer = False
        self.isPeriodDetails = False

    def startElement(self, name, attrs):
        if name in self.boxscore:
            self.isBoxScore = True
            self.insertdata = []
        elif name in ['period-details', 'scoring-summaries', 'half-details']:
            self.isPeriodDetails = True
        elif name == 'season':
            self.season = attrs.get('season')
            if self.season is None:
                self.season = attrs.get('year')
            self.teams = get_teams(c, league)
        elif name == 'gamecode':
            self.gamecode = attrs.get('global-id')
            if self.gamecode is None:
                self.gamecode = attrs.get('global-code')
            cid = get_finalstats(c, self.gamecode)
            if cid is not None:
                self.id = int(cid[0] or 0)
            else:
                self.id = 0
        elif name == 'gametype':
            self.gametype = re.escape(attrs.get('type'))
        elif name == 'game-type':
            self.gametype = re.escape(attrs.get('description'))
        elif name == 'stadium':
            self.stadium_name = attrs.get('name')
            if self.stadium_name is None:
                self.stadium_name = ''
            else:
                self.stadium_name = replace_nonascii(self.stadium_name)
            self.stadium_city = attrs.get('city')
            if self.stadium_city is None:
                self.stadium_city = ''
            else:
                self.stadium_city = replace_nonascii(self.stadium_city)
            self.stadium_state = attrs.get('state')
            if self.stadium_state is None:
                self.stadium_state = ''
            else:
                self.stadium_state = replace_nonascii(self.stadium_state)
            self.stadium_country = attrs.get('country')
            if self.stadium_country is None:
                self.stadium_country = ''
            else:
                self.stadium_country = replace_nonascii(self.stadium_country)
        elif name == 'date' and self.isBoxScore and not self.isPeriodDetails:
            self.date = attrs.get('year') + '-' + attrs.get('month') + '-' + attrs.get('date')
        elif name == 'time' and self.isBoxScore and not self.isPeriodDetails:
            hour = attrs.get('hour')
            if hour == '':
                hour = "00"
            minute = attrs.get('minute')
            if minute == '':
                minute = "00"
            self.time = hour + ':' + minute + ':00'
        elif name == 'gamestate':
            self.gamestate = attrs.get('status')
        elif name in ['visiting-team', 'visiting-team-stats', 'visiting-player-stats',
                      'baseball-mlb-boxscore-visiting-team-pitching-lineup',
                      'baseball-mlb-boxscore-visiting-team-batting-lineup'] and not self.isPeriodDetails:
            self.isAway = True
        elif name in ['goaltenders', 'skaters', 'bench', 'players', 'team-stats'] and attrs.get('team') is not None:
            if attrs.get('team') == 'visitors':
                self.isAway = True
            if attrs.get('team') == 'home':
                self.isHome = True
        elif name in ['home-team', 'home-team-stats', 'home-player-stats',
                      'baseball-mlb-boxscore-home-team-pitching-lineup',
                      'baseball-mlb-boxscore-home-team-batting-lineup'] and not self.isPeriodDetails:
            self.isHome = True
        elif name == 'team-info' and (self.isAway or self.isHome) and not self.isPeriodDetails:
            if self.isAway:
                self.away_team_name = replace_nonascii(attrs.get('display-name'))
                self.away_team_alias = re.escape(attrs.get('alias'))
                self.away_team_global_id = attrs.get('global-id')
            if self.isHome:
                self.home_team_name = replace_nonascii(attrs.get('display-name'))
                self.home_team_alias = re.escape(attrs.get('alias'))
                self.home_team_global_id = attrs.get('global-id')
        elif name == 'team-name' and (self.isAway or self.isHome) and not self.isPeriodDetails:
            if self.isAway:
                self.away_team_name = replace_nonascii(attrs.get('name'))
                self.away_team_alias = re.escape(attrs.get('alias'))
            if self.isHome:
                self.home_team_name = replace_nonascii(attrs.get('name'))
                self.home_team_alias = re.escape(attrs.get('alias'))
        elif name == 'team-code' and (self.isAway or self.isHome) and not self.isPeriodDetails:
            if self.isAway:
                self.away_team_global_id = attrs.get('global-id')
            if self.isHome:
                self.home_team_global_id = attrs.get('global-id')
        elif name == 'team-city' and (self.isAway or self.isHome) and not self.isPeriodDetails:
            if self.isAway:
                self.away_team_city = replace_nonascii(attrs.get('city'))
            if self.isHome:
                self.home_team_city = replace_nonascii(attrs.get('city'))
        elif name == 'linescore':
            if self.isAway:
                self.away_team_score = attrs.get('score')
            if self.isHome:
                self.home_team_score = attrs.get('score')
        elif name == 'home-score' and not self.isPeriodDetails:
            if attrs.get('type') == 'runs':
                self.home_team_score = attrs.get('number')
            self.scores.append("("
                               + str(0) +
                               ",'"
                               + self.gamecode +
                               "','"
                               + attrs.get('type') +
                               "','"
                               + attrs.get('number') +
                               "','"
                               + self.home_team_global_id +
                               "')")
        elif name == 'visiting-score' and not self.isPeriodDetails:
            if attrs.get('type') == 'runs':
                self.away_team_score = attrs.get('number')
            self.scores.append("("
                               + str(0) +
                               ",'"
                               + self.gamecode +
                               "','"
                               + attrs.get('type') +
                               "','"
                               + attrs.get('number') +
                               "','"
                               + self.away_team_global_id +
                               "')")
        elif name == 'quarter':
            if self.isHome:
                self.team_global_id = self.home_team_global_id
            if self.isAway:
                self.team_global_id = self.away_team_global_id
            quarter = attrs.get('quarter')
            if quarter == '1':
                self.quarter = (quarter + 'st')
            if quarter == '2':
                self.quarter = (quarter + 'nd')
            if quarter == '3':
                self.quarter = (quarter + 'rd')
            if quarter > '3':
                self.quarter = (quarter + 'th')
            self.score = attrs.get('score')
            self.num1 = attrs.get('team-fouls')
            self.linescores.append("("
                                   + str(0) +
                                   ",'"
                                   + str(self.quarter) +
                                   "','"
                                   + str(self.score) +
                                   "','"
                                   + str(self.num1) +
                                   "','"
                                   + str(self.num2) +
                                   "','"
                                   + str(self.gamecode) +
                                   "','"
                                   + str(self.team_global_id) +
                                   "')")
        elif name == 'period':
            if self.isHome:
                self.team_global_id = self.home_team_global_id
            if self.isAway:
                self.team_global_id = self.away_team_global_id
            quarter = attrs.get('period')
            if quarter == '1':
                self.quarter = (quarter + 'st')
            if quarter == '2':
                self.quarter = (quarter + 'nd')
            if quarter == '3':
                self.quarter = (quarter + 'rd')
            if quarter > '3':
                self.quarter = (quarter + 'th')
            self.score = attrs.get('score')
            self.num1 = attrs.get('shots')
            self.linescores.append("("
                                   + str(0) +
                                   ",'"
                                   + str(self.quarter) +
                                   "','"
                                   + str(self.score) +
                                   "','"
                                   + str(self.num1) +
                                   "','"
                                   + str(self.num2) +
                                   "','"
                                   + str(self.gamecode) +
                                   "','"
                                   + str(self.team_global_id) +
                                   "')")
        elif name == 'half':
            if self.isHome:
                self.team_global_id = self.home_team_global_id
            if self.isAway:
                self.team_global_id = self.away_team_global_id
            quarter = attrs.get('half')
            if quarter == '1':
                self.quarter = (quarter + 'st')
            if quarter == '2':
                self.quarter = (quarter + 'nd')
            if quarter == '3':
                self.quarter = (quarter + 'rd')
            self.score = attrs.get('score')
            self.num1 = ''
            self.linescores.append("("
                                   + str(0) +
                                   ",'"
                                   + str(self.quarter) +
                                   "','"
                                   + str(self.score) +
                                   "','"
                                   + str(self.num1) +
                                   "','"
                                   + str(self.num2) +
                                   "','"
                                   + str(self.gamecode) +
                                   "','"
                                   + str(self.team_global_id) +
                                   "')")
        elif name == 'inning':
            if self.isHome:
                self.team_global_id = self.home_team_global_id
            if self.isAway:
                self.team_global_id = self.away_team_global_id
            quarter = attrs.get('number')
            if quarter == '1':
                self.quarter = (quarter + 'st')
            if quarter == '2':
                self.quarter = (quarter + 'nd')
            if quarter == '3':
                self.quarter = (quarter + 'rd')
            if quarter > '3':
                self.quarter = (quarter + 'th')
            self.score = attrs.get('score')
            self.num1 = ''
            self.linescores.append("("
                                   + str(0) +
                                   ",'"
                                   + str(self.quarter) +
                                   "','"
                                   + str(self.score) +
                                   "','"
                                   + str(self.num1) +
                                   "','"
                                   + str(self.num2) +
                                   "','"
                                   + str(self.gamecode) +
                                   "','"
                                   + str(self.team_global_id) +
                                   "')")
        elif name == 'team-stats':
            self.isTeam = True
            if attrs.get('team') == 'home':
                self.isHome = True
            if attrs.get('team') == 'visitors':
                self.isAway = True
        elif name not in ['technical-fouls-details', 'defensive-3-seconds-details', 'home-team-stats',
                          'visiting-team-stats'] and self.isTeam:
            self.stat_type = name
            for attrName in attrs.keys():
                self.stat = re.escape(attrName)
                self.value = re.escape(attrs.get(attrName))
                if self.isHome:
                    home = 't'
                    self.team_global_id = self.home_team_global_id
                if self.isAway:
                    home = 'f'
                    self.team_global_id = self.away_team_global_id
                self.teamstats.append("("
                                      + str(0) +
                                      ",'"
                                      + str(self.stat_type) +
                                      "','"
                                      + str(self.stat) +
                                      "','"
                                      + str(self.value) +
                                      "','"
                                      + str(self.gamecode) +
                                      "','"
                                      + str(self.team_global_id) +
                                      "','"
                                      + str(home) +
                                      "')")
                self.stat = ''
                self.value = ''
            self.stat_type = ''
        elif name in ['player-stats', 'goaltender', 'skater', 'player', 'baseball-mlb-boxscore-batting-lineup',
                      'baseball-mlb-boxscore-pitching-lineup'] and not self.isPeriodDetails:
            self.split = name
            self.isPlayer = True
        elif name == 'player-code' and self.isPlayer and not self.isPeriodDetails:
            self.player_global_id = attrs.get('global-id')
        elif name not in ['fielding', 'name', 'player-position', 'player-number', 'player-code', 'visiting-player-stats'
            , 'home-player-stats', 'stint-details', 'stint-detail',
                          'period-shot-totals'] and self.isPlayer and not self.isPeriodDetails and league_name != 'nfl':
            self.stat_type = name
            for attrName in attrs.keys():
                self.stat = re.escape(attrName)
                self.value = re.escape(attrs.get(attrName))
                if self.isHome:
                    self.team_global_id = self.home_team_global_id
                if self.isAway:
                    self.team_global_id = self.away_team_global_id
                self.playerstats.append("("
                                        + str(0) +
                                        ",'"
                                        + str(self.stat_type) +
                                        "','"
                                        + str(self.stat) +
                                        "','"
                                        + str(self.value) +
                                        "','"
                                        + str(self.gamecode) +
                                        "','"
                                        + str(self.player_global_id) +
                                        "','"
                                        + str(self.team_global_id) +
                                        "','"
                                        + str(self.split) +
                                        "')")
                self.stat = ''
                self.value = ''
            self.stat_type = ''
        elif name not in ['name', 'player-code', 'visiting-player-stats', 'home-player-stats', 'stint-details',
                          'stint-detail',
                          'period-shot-totals'] and self.isPlayer and not self.isPeriodDetails and league_name == 'nfl':
            self.playerstat = []
            self.stat_type = name
            for attrName in attrs.keys():
                stats = Stats()
                stats.stat_type = self.stat_type
                stats.stat = re.escape(attrName)
                stats.value = re.escape(attrs.get(attrName))
                self.playerstat.append(stats)
        return

    def endElement(self, name):
        if name in self.boxscore:
            self.isBoxScore = False
            self.competitions.append("("
                                     + str(self.id) +
                                     ",'"
                                     + str(self.gamecode) +
                                     "','"
                                     + str(self.gametype) +
                                     "','"
                                     + str(self.stadium_name) +
                                     "','"
                                     + str(self.stadium_city) +
                                     "','"
                                     + str(self.stadium_state) +
                                     "','"
                                     + str(self.stadium_country) +
                                     "','"
                                     + str(self.date + ' ' + self.time) +
                                     "','"
                                     + str(self.gamestate) +
                                     "','"
                                     + str(self.away_team_name) +
                                     "','"
                                     + str(self.away_team_city) +
                                     "','"
                                     + str(self.away_team_alias) +
                                     "','"
                                     + str(self.away_team_global_id) +
                                     "','"
                                     + str(self.away_team_score) +
                                     "','"
                                     + str(self.home_team_name) +
                                     "','"
                                     + str(self.home_team_city) +
                                     "','"
                                     + str(self.home_team_alias) +
                                     "','"
                                     + str(self.home_team_global_id) +
                                     "','"
                                     + str(self.home_team_score) +
                                     "','"
                                     + str(self.season) +
                                     "','"
                                     + str(league_name) +
                                     "')")
            data = str.join(',', self.competitions)
            insert_competitions(c, data)
            self.competitions = []
            cid = get_score(c, self.gamecode)
            if cid is None:
                self.id = 0
            else:
                self.id = cid[0]
            self.insertdata.append("("
                                   + str(self.id) +
                                   ","
                                   + str(league_id) +
                                   ",'"
                                   + str(self.date + ' ' + self.time) +
                                   "','"
                                   + str(self.gamestate) +
                                   "','"
                                   + str(self.home_team_alias) +
                                   "',"
                                   + str(find_value_in_array2args(self.teams, self.home_team_global_id)) +
                                   ","
                                   + str(self.home_team_score) +
                                   ",'"
                                   + str(self.away_team_alias) +
                                   "',"
                                   + str(find_value_in_array2args(self.teams, self.away_team_global_id)) +
                                   ","
                                   + str(self.away_team_score) +
                                   ",'"
                                   + str(self.gamecode) +
                                   "','"
                                   "','"
                                   "')")
            data = str.join(',', self.insertdata)
            if debug:
                print data
            insert_boxscores(c, data)
            self.insertdata = []
        elif name in ['period-details', 'scoring-summaries', 'half-details']:
            self.isPeriodDetails = False
        elif name in ['visiting-team', 'visiting-team-stats', 'visiting-player-stats',
                      'baseball-mlb-boxscore-visiting-team-pitching-lineup',
                      'baseball-mlb-boxscore-visiting-team-batting-lineup'] and not self.isPeriodDetails:
            self.isAway = False
        elif name in ['home-team', 'home-team-stats', 'home-player-stats',
                      'baseball-mlb-boxscore-home-team-pitching-lineup',
                      'baseball-mlb-boxscore-home-team-batting-lineup'] and not self.isPeriodDetails:
            self.isHome = False
        elif name in ['goaltenders', 'skaters', 'bench', 'players']:
            self.isAway = False
            self.isHome = False
        elif name in ['linescore', 'innings']:
            if self.id == 0:
                data = str.join(',', self.linescores)
                insert_linescores(c, data)
                self.linescores = []
        elif name in ['home-score', 'visiting-score']:
            if self.id == 0:
                data = str.join(',', self.scores)
                insert_scores(c, data)
                self.scores = []
        elif name == 'team-stats':
            self.isAway = False
            self.isHome = False
            self.isTeam = False
            if self.id == 0:
                data = str.join(',', self.teamstats)
                insert_teamstats(c, data)
                self.teamstats = []
        elif name in ['player-stats', 'goaltender', 'skater', 'player', 'baseball-mlb-boxscore-batting-lineup',
                      'baseball-mlb-boxscore-pitching-lineup'] and not self.isPeriodDetails:
            self.isPlayer = False
            if self.id == 0:
                data = str.join(',', self.playerstats)
                insert_playerstats(c, data)
                self.playerstats = []
        elif name not in ['name', 'player-code', 'visiting-player-stats', 'home-player-stats', 'stint-details',
                          'stint-detail',
                          'period-shot-totals'] and self.isPlayer and not self.isPeriodDetails and league_name == 'nfl':
            if self.isHome:
                self.team_global_id = self.home_team_global_id
            if self.isAway:
                self.team_global_id = self.away_team_global_id
            for stats in self.playerstat:
                self.playerstats.append("("
                                        + str(0) +
                                        ",'"
                                        + str(stats.stat_type) +
                                        "','"
                                        + str(stats.stat) +
                                        "','"
                                        + str(stats.value) +
                                        "','"
                                        + str(self.gamecode) +
                                        "','"
                                        + str(self.player_global_id) +
                                        "','"
                                        + str(self.team_global_id) +
                                        "','"
                                        + str(self.split) +
                                        "')")


if __name__ == "__main__":
    try:
        if os.access(os.path.expanduser("~/.lockfile.finalstats.lock"), os.F_OK):
            # if the lockfile is already there then check the PID number
            # in the lock file
            pidfile = open(os.path.expanduser("~/.lockfile.finalstats.lock"), "r")
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
                os.remove(os.path.expanduser("~/.lockfile.finalstats.lock"))
        else:
            pidfile = open(os.path.expanduser("~/.lockfile.finalstats.lock"), "w")
            pidfile.write("%s" % os.getpid())
            pidfile.close()
            cc = db_open()
            c = cc[0]
            conn = cc[1]
            parser = make_parser()
            for final in finalstats_files:
                if debug:
                    print final[0]
                files = glob.glob(path + final[0])
                league_name = final[1]
                league_id = final[2]
                league = final[3]
                for file in files:
                    if os.path.exists(file):
                        curHandler = NBAHandler()
                        parser.setContentHandler(curHandler)
                        parser.parse(open(file))

            db_close(c, conn)

            os.remove(os.path.expanduser("~/.lockfile.finalstats.lock"))
    except:
        if debug:
            print traceback.format_exc()
        else:
            send_mail(traceback.format_exc())
        os.remove(os.path.expanduser("~/.lockfile.finalstats.lock"))
        sys.exit(1)
