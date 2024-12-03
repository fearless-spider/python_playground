#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from statsfiles import live_files, schedule_files
from statsutils import find_value_in_array2args, find_value_in_array4args, path, debug, send_mail
from statsdb import db_open, db_close, get_stands, get_teams, insert_standings

__author__ = 'fearless'


class NBAHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '2')
        elif name == 'nba-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name == 'wins' or name == 'losses' or name == 'games-back':
            self.group = name
            self.type = ''
            self.num = attrs.get('number')
            self.num2 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.num = attrs.get('place')
            self.num2 = ''
        elif name == 'points-for-per-game' or name == 'points-against-per-game':
            self.group = name
            self.type = ''
            self.num = attrs.get('points')
            self.num2 = ''
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.num = attrs.get('games')
            self.num2 = ''
        elif name == 'conference-seed':
            self.group = name
            self.type = ''
            self.num = attrs.get('seed')
            self.num2 = ''
        elif name == 'conference-games-back':
            self.group = name
            self.type = ''
            self.num = attrs.get('games')
            self.num2 = ''
        elif name == 'eliminated-from-playoffs':
            self.group = name
            self.type = ''
            self.num = attrs.get('eliminated')
            self.num2 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'nba-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            print data
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name == 'wins' or name == 'losses' \
                or name == 'games-back' \
                or name == 'winning-percentage' \
                or name == 'place' \
                or name == 'points-for-per-game' or name == 'points-against-per-game' \
                or name == 'win-loss-record' \
                or name == 'streak' \
                or name == 'conference-seed' \
                or name == 'conference-games-back' \
                or name == 'eliminated-from-playoffs':
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class WNBAHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '5082')
        elif name == 'wnba-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name == 'wins' or name == 'losses' or name == 'games-back':
            self.group = name
            self.type = ''
            self.num = attrs.get('number')
            self.num2 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.num = attrs.get('place')
            self.num2 = ''
        elif name == 'points-for-per-game' or name == 'points-against-per-game':
            self.group = name
            self.type = ''
            self.num = attrs.get('points')
            self.num2 = ''
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.num = attrs.get('games')
            self.num2 = ''
        elif name == 'conference-seed':
            self.group = name
            self.type = ''
            self.num = attrs.get('seed')
            self.num2 = ''
        elif name == 'conference-games-back':
            self.group = name
            self.type = ''
            self.num = attrs.get('games')
            self.num2 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'wnba-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name == 'wins' or name == 'losses' \
                or name == 'games-back' \
                or name == 'winning-percentage' \
                or name == 'place' \
                or name == 'points-for-per-game' or name == 'points-against-per-game' \
                or name == 'win-loss-record' \
                or name == 'streak' \
                or name == 'conference-seed' \
                or name == 'conference-games-back':
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class CBKHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '128')
        elif name == 'cbk-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name == 'wins' or name == 'losses':
            self.group = name
            self.type = ''
            self.num = attrs.get('number')
            self.num2 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.num = attrs.get('place')
            self.num2 = ''
        elif name == 'ranking':
            self.group = name
            self.type = ''
            self.num = attrs.get('ranking')
            self.num2 = ''
        elif name == 'points-for' or name == 'points-against':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('number')
            self.num2 = ''
        elif name == 'sos':
            self.group = name
            self.type = ''
            self.num = attrs.get('rank')
            self.num2 = attrs.get('sos')
        elif name == 'rpi':
            self.group = name
            self.type = ''
            self.num = attrs.get('rank')
            self.num2 = attrs.get('rpi')
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.num = attrs.get('games')
            self.num2 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'cbk-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name == 'wins' or name == 'losses' \
                or name == 'winning-percentage' \
                or name == 'place' \
                or name == 'ranking' \
                or name == 'points-for' or name == 'points-against' \
                or name == 'rpi' or name == 'sos' \
                or name == 'win-loss-record' \
                or name == 'streak':
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class WCBKHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '129')
        elif name == 'wcbk-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name == 'wins' or name == 'losses':
            self.group = name
            self.type = ''
            self.num = attrs.get('number')
            self.num2 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.num = attrs.get('place')
            self.num2 = ''
        elif name == 'ranking':
            self.group = name
            self.type = ''
            self.num = attrs.get('ranking')
            self.num2 = ''
        elif name == 'points-for' or name == 'points-against':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('number')
            self.num2 = ''
        elif name == 'sos':
            self.group = name
            self.type = ''
            self.num = attrs.get('rank')
            self.num2 = attrs.get('sos')
        elif name == 'rpi':
            self.group = name
            self.type = ''
            self.num = attrs.get('rank')
            self.num2 = attrs.get('rpi')
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.num = attrs.get('games')
            self.num2 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'wcbk-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name == 'wins' or name == 'losses' \
                or name == 'winning-percentage' \
                or name == 'place' \
                or name == 'ranking' \
                or name == 'points-for' or name == 'points-against' \
                or name == 'rpi' or name == 'sos' \
                or name == 'win-loss-record' \
                or name == 'streak':
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class NFLHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '3')
        elif name == 'football-nfl-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name in ['wins', 'losses', 'ties', 'points-for', 'points-against', 'games-back', 'wc-games-back']:
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('number')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('place')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.name = attrs.get('name')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
            self.num3 = attrs.get('ties')
            self.num4 = ''
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.name = ''
            self.num = attrs.get('games')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'eliminated-from-playoffs':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('eliminated')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'football-nfl-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name in ['wins', 'losses', 'ties', 'points-for', 'points-against', 'games-back', 'wc-games-back',
                      'winning-percentage', 'place', 'win-loss-record', 'streak', 'eliminated-from-playoffs']:
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class CFBHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '130')
        elif name == 'cfb-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name in ['wins', 'losses']:
            self.group = name
            self.type = ''
            self.num = attrs.get('number')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'ranking':
            self.group = name
            self.type = ''
            self.num = attrs.get('ranking')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.num = attrs.get('place')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'points-for' or name == 'points-against':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('number')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
            self.num3 = attrs.get('percentage')
            self.num4 = ''
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.num = attrs.get('games')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'cfb-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name in ['wins', 'losses', 'winning-percentage', 'place', 'ranking', 'points-for', 'points-against',
                      'win-loss-record'
            , 'streak']:
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class MLBHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '5')
        elif name == 'baseball-mlb-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name in ['wins', 'losses', 'games-back', 'wc-games-back']:
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('number')
            self.num2 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
        elif name == 'division-rank':
            self.group = name
            self.type = 'rank'
            self.name = ''
            self.num = attrs.get('rank')
            self.num2 = ''
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.name = attrs.get('name')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.name = ''
            self.num = attrs.get('games')
            self.num2 = ''
        elif name == 'eliminated-from-playoffs':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('eliminated')
            self.num2 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'baseball-mlb-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name in ['wins', 'losses', 'games-back', 'wc-games-back', 'winning-percentage', 'division-rank',
                      'win-loss-record', 'streak', 'eliminated-from-playoffs']:
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class NHLHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            self.teams = get_teams(c, '4')
        elif name == 'hockey-nhl-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-code':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name in ['wins', 'losses', 'ties', 'overtime-losses', 'shootout-losses', 'team-points']:
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('number')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('place')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.name = attrs.get('name')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
            self.num3 = attrs.get('overtime-losses')
            self.num4 = attrs.get('shootout-losses')
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.name = ''
            self.num = attrs.get('games')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name in ['goals-for', 'goals-against']:
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('goals')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'hockey-nhl-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-code':
            self.isTeamCode = False
        elif name in ['wins', 'losses', 'ties', 'overtime-losses', 'shootout-losses', 'team-points',
                      'winning-percentage', 'place', 'win-loss-record', 'streak', 'goals-for', 'goals-against']:
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


class MLSHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.team_id = 0
        self.global_id = 0
        self.group = ''
        self.type = ''
        self.name = ''
        self.num = ''
        self.num2 = ''
        self.num3 = ''
        self.num4 = ''
        self.season = ''
        self.league = ''
        self.insertdata = []
        self.teams = []
        self.stands = []

        self.isSeason = False
        self.isTeam = False
        self.isTeamCode = False

    def startElement(self, name, attrs):
        if name == 'league':
            self.league = attrs.get('alias')
        elif name == 'season':
            self.isSeason = True
            self.season = attrs.get('year')
            for live in schedule_files:
                if live[2] == self.league.lower():
                    self.teams = get_teams(c, str(live[0]))
        elif name == 'ifb-team-standings':
            self.isTeam = True
            self.insertdata = []
        elif name == 'team-info':
            self.global_id = attrs.get('global-id')
            self.team_id = int(find_value_in_array2args(self.teams, self.global_id) or 0)
            self.stands = get_stands(c, self.team_id, self.season)
        elif name in ['wins', 'losses', 'ties']:
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('number')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'winning-percentage':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('percentage')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'place':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('place')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'games-played':
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('games')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name == 'points':
            self.group = name
            self.type = 'points'
            self.name = ''
            self.num = attrs.get('points')
            self.num2 = attrs.get('points-per-game')
            self.num3 = attrs.get('penalty-points')
            self.num4 = ''
        elif name == 'win-loss-record':
            self.group = name
            self.type = attrs.get('type')
            self.name = attrs.get('name')
            self.num = attrs.get('wins')
            self.num2 = attrs.get('losses')
            self.num3 = attrs.get('goals')
            self.num4 = attrs.get('goals-against')
        elif name == 'streak':
            self.group = name
            self.type = attrs.get('kind')
            self.name = ''
            self.num = attrs.get('games')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        elif name in ['goals-for', 'goals-against']:
            self.group = name
            self.type = ''
            self.name = ''
            self.num = attrs.get('goals')
            self.num2 = ''
            self.num3 = ''
            self.num4 = ''
        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'ifb-team-standings':
            self.isTeam = False
            data = str.join(',', self.insertdata)
            insert_standings(c, data)
        elif name == 'team-info':
            self.isTeamCode = False
        elif name in ['wins', 'losses', 'ties', 'points', 'winning-percentage', 'place', 'win-loss-record', 'streak',
                      'goals-for', 'goals-against', 'games-played']:
            if self.team_id > 0:
                self.id = int(find_value_in_array4args(self.stands, self.group, self.type, self.name) or 0)
                self.insertdata.append("("
                                       + str(self.id) +
                                       ",'"
                                       + str(self.group) +
                                       "','"
                                       + str(self.type) +
                                       "','"
                                       + str(self.name) +
                                       "','"
                                       + str(self.num) +
                                       "','"
                                       + str(self.num2) +
                                       "','"
                                       + str(self.num3) +
                                       "','"
                                       + str(self.num4) +
                                       "',"
                                       + str(self.team_id) +
                                       ",'"
                                       + str(self.season) +
                                       "','"
                                       + str(self.global_id) +
                                       "')")


if __name__ == "__main__":
    if os.access(os.path.expanduser("~/.lockfile.standing.lock"), os.F_OK):
        # if the lockfile is already there then check the PID number
        # in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.standing.lock"), "r")
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
            os.remove(os.path.expanduser("~/.lockfile.standing.lock"))
    else:
        pidfile = open(os.path.expanduser("~/.lockfile.standing.lock"), "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close

        try:
            cc = db_open()
            c = cc[0]
            conn = cc[1]

            parser = make_parser()
            curHandler = NBAHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "NBA_TEAM_STANDINGS.XML"))

            curHandler = WNBAHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "WNBA_TEAM_STANDINGS.XML"))

            curHandler = CBKHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "CBK_TEAM_STANDINGS.XML"))

            curHandler = WCBKHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "WCBK_TEAM_STANDINGS.XML"))

            curHandler = MLBHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "MLB_TEAM_STANDINGS.XML"))

            curHandler = NFLHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "NFL_TEAM_STANDINGS.XML"))

            curHandler = CFBHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "CFB_TEAM_STANDINGS.XML"))

            curHandler = NHLHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "NHL_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "BUND_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "FRAN_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "EPL_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "CHLG_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "FMF_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "SERI_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "LIGA_TEAM_STANDINGS.XML"))

            curHandler = MLSHandler()
            parser.setContentHandler(curHandler)
            parser.parse(open(path + "MLS_TEAM_STANDINGS.XML"))

            db_close(c, conn)
            os.remove(os.path.expanduser("~/.lockfile.standing.lock"))
        except:
            if debug:
                print traceback.format_exc()
            else:
                send_mail("standings", traceback.format_exc())
            os.remove(os.path.expanduser("~/.lockfile.standing.lock"))
            sys.exit(1)
