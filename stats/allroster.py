#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import sys
from statsfiles import allroster_files
from statsutils import find_value_in_array2args, replace_nonascii, path, send_mail, debug
from statsdb import db_open, db_close, get_teams, get_players, insert_players

__author__ = 'fearless'


class NBAHandler(ContentHandler):
    rosters = ['wnba-rosters', 'wcbk-rosters', 'nba-rosters', 'cbk-rosters', 'cfb-rosters', 'nhl-rosters',
               'baseball-mlb-rosters', 'nfl-rosters', 'ifb-soccer-roster']
    roster = ['wnba-roster', 'wcbk-roster', 'nba-roster', 'cbk-roster', 'cfb-roster', 'nhl-roster',
              'baseball-mlb-rosters-team', 'nfl-roster', 'ifb-team-roster']
    player = ['wnba-player', 'wcbk-player', 'nba-player', 'cbk-player', 'cfb-player', 'nhl-roster-player',
              'baseball-mlb-rosters-player', 'nfl-player', 'ifb-roster-player']

    id = 0
    league_name = ''
    global_id = 0
    player_global_id = 0
    firstname = ''
    lastname = ''
    team_id = 0
    season = ''
    height = 0
    weight = 0
    birthdate = ''
    birthcity = ''
    birthstate = ''
    birthcountry = ''
    number = 0
    position = ''
    status = 1
    school = ''
    highschool_name = ''
    highschool_city = ''
    first_year = ''
    rookie_year = ''
    experience = 0
    suspended = 0
    Insert = False
    insertdata = []
    teams = []
    groups = []

    isSeason = False
    isNBARosters = False
    isNBARoster = False
    isNBAPlayer = False
    isDraft = False

    def __init__(self):
        self.rosters = ['wnba-rosters', 'wcbk-rosters', 'nba-rosters', 'cbk-rosters', 'cfb-rosters', 'nhl-rosters',
                        'baseball-mlb-rosters', 'nfl-rosters', 'ifb-soccer-roster']
        self.roster = ['wnba-roster', 'wcbk-roster', 'nba-roster', 'cbk-roster', 'cfb-roster', 'nhl-roster',
                       'baseball-mlb-rosters-team', 'nfl-roster', 'ifb-team-roster']
        self.player = ['wnba-player', 'wcbk-player', 'nba-player', 'cbk-player', 'cfb-player', 'nhl-roster-player',
                       'baseball-mlb-rosters-player', 'nfl-player', 'ifb-roster-player']

        self.id = 0
        self.league_name = ''
        self.global_id = 0
        self.player_global_id = 0
        self.firstname = ''
        self.lastname = ''
        self.team_id = 0
        self.season = ''
        self.height = 0
        self.weight = 0
        self.birthdate = ''
        self.birthcity = ''
        self.birthstate = ''
        self.birthcountry = ''
        self.number = 0
        self.position = ''
        self.status = 1
        self.school = ''
        self.highschool_name = ''
        self.highschool_city = ''
        self.first_year = ''
        self.rookie_year = ''
        self.experience = 0
        self.suspended = 0
        self.Insert = False
        self.insertdata = []
        self.teams = []
        self.groups = []

        self.isSeason = False
        self.isNBARosters = False
        self.isNBARoster = False
        self.isNBAPlayer = False
        self.isDraft = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            if self.season is None:
                self.season = attrs.get('year')
            self.teams = get_teams(c, self.league_name)
            self.players = get_players(c, self.season)
        elif name in self.rosters:
            self.isNBARosters = True
        elif name in self.roster:
            self.isNBARoster = True
            self.insertdata = []
            self.team_id = 0
        elif name in ['team-code', 'team-info'] and not self.isNBAPlayer and not self.isDraft:
            self.global_id = attrs.get('global-id')
        elif name in self.player:
            self.isNBAPlayer = True
            self.id = 0
            self.global_id = 0
            self.firstname = ''
            self.lastname = ''
            self.height = 0
            self.weight = 0
            self.birthdate = ''
            self.birthcity = ''
            self.birthstate = ''
            self.birthcountry = ''
            self.number = 0
            self.position = ''
            self.status = 1
            self.school = ''
            self.highschool_name = ''
            self.highschool_city = ''
            self.first_year = ''
            self.rookie_year = ''
            self.experience = 0
            self.suspended = 0
        elif name == 'name':
            self.firstname = attrs.get('first-name')
            if self.firstname is not None:
                self.firstname = replace_nonascii(self.firstname)
            self.lastname = attrs.get('last-name')
            if self.lastname is not None:
                self.lastname = replace_nonascii(self.lastname)
        elif name == 'player-position':
            self.position = attrs.get('position')
            if self.position is None:
                self.position = attrs.get('english')
        elif name == 'player-number':
            self.number = attrs.get('number')
        elif name == 'player-status':
            self.status = 1
            if attrs.get('status').lower() == 'false':
                self.status = 0
        elif name == 'player-code':
            self.player_global_id = attrs.get('global-id')
        elif name == 'height':
            self.height = attrs.get('inches')
        elif name == 'weight':
            self.weight = attrs.get('pounds')
        elif name == 'birth-date':
            self.birthdate = attrs.get('year') + '-' + attrs.get('month') + '-' + attrs.get('date')
        elif name == 'birth-loc':
            self.birthcity = attrs.get('city')
            if self.birthcity is not None:
                self.birthcity = replace_nonascii(self.birthcity)
            self.birthstate = attrs.get('state')
            if self.birthstate is not None:
                self.birthstate = replace_nonascii(self.birthstate)
            self.birthcountry = attrs.get('country')
            if self.birthcountry is not None:
                self.birthcountry = replace_nonascii(self.birthcountry)
        elif name in ['birth-city', 'hometown']:
            self.birthcity = attrs.get('city')
            if self.birthcity is not None:
                self.birthcity = replace_nonascii(self.birthcity)
        elif name in ['birth-state', 'home-state', 'birth-state-country']:
            self.birthstate = attrs.get('state')
            if self.birthstate is not None:
                self.birthstate = replace_nonascii(self.birthstate)
        elif name in 'birth-country':
            self.birthcountry = attrs.get('country')
            if self.birthcountry is not None:
                self.birthcountry = replace_nonascii(self.birthcountry)
        elif name == 'hometown-country':
            self.birthcountry = attrs.get('name')
            if self.birthcountry is not None:
                self.birthcountry = replace_nonascii(self.birthcountry)
        elif name == 'school':
            self.school = attrs.get('school')
            if self.school is not None:
                self.school = replace_nonascii(self.school)
        elif name == 'high-school':
            self.highschool_name = attrs.get('name')
            if self.highschool_name is not None:
                self.highschool_name = replace_nonascii(self.highschool_name)
            self.highschool_city = attrs.get('city')
            if self.highschool_city is not None:
                self.highschool_city = replace_nonascii(self.highschool_city)
        elif name == 'first-year':
            self.first_year = attrs.get('year')
            self.rookie_year = attrs.get('rookie-year')
        elif name == 'experience':
            self.experience = attrs.get('experience')
            if self.experience is None:
                self.experience = 0
        elif name == 'suspended':
            if attrs.get('suspended').lower() == 'true':
                self.suspended = 1
        elif name == 'draft-info':
            self.isDraft = True

        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name in self.rosters:
            self.isNBARosters = False
        elif name in self.roster:
            self.isNBARoster = False
            data = str.join(',', self.insertdata)
            # if self.team_id == 3:
            #    print insert_players(c, data)
            insert_players(c, data)
        elif name in ['team-code', 'team-info'] and not self.isNBAPlayer and not self.isDraft:
            sid = find_value_in_array2args(self.teams, self.global_id)
            if sid is not None:
                self.team_id = int(sid or 0)
                self.Insert = True
            else:
                self.Insert = False
        elif name == 'draft-info':
            self.isDraft = False
        elif name in self.player and self.Insert:
            self.isNBAPlayer = False
            self.id = int(find_value_in_array2args(self.players, self.player_global_id) or 0)
            self.insertdata.append("("
                                   + str(self.id) +
                                   ",'"
                                   + self.firstname +
                                   "','"
                                   + self.lastname +
                                   "',"
                                   + str(self.team_id) +
                                   ","
                                   + str(int(self.height or 0)) +
                                   ","
                                   + str(int(self.weight or 0)) +
                                   ",'"
                                   + str(self.birthdate) +
                                   "','"
                                   + self.birthcity +
                                   "','"
                                   + self.birthstate +
                                   "','"
                                   + self.birthcountry +
                                   "',"
                                   + str(int(self.number or 0)) +
                                   ",'"
                                   + self.position +
                                   "',"
                                   + str(self.status) +
                                   ",'"
                                   + str(self.player_global_id) +
                                   "','"
                                   + self.school +
                                   "','"
                                   + self.highschool_name +
                                   "','"
                                   + self.highschool_city +
                                   "','"
                                   + str(self.first_year) +
                                   "','"
                                   + str(self.rookie_year) +
                                   "',"
                                   + str(self.experience) +
                                   ","
                                   + str(self.suspended) +
                                   ",'"
                                   + str(self.season) +
                                   "')")


if __name__ == "__main__":
    try:
        cc = db_open()
        c = cc[0]
        conn = cc[1]

        parser = make_parser()
        for file in allroster_files:
            if debug:
                print file
            if os.path.exists(path + file[0]):
                curHandler = NBAHandler()
                curHandler.league_name = file[1]
                parser.setContentHandler(curHandler)
                parser.parse(open(path + file[0]))

        db_close(c, conn)
    except:
        if debug:
            print traceback.format_exc()
        else:
            send_mail("allroster", traceback.format_exc())
        sys.exit(1)
