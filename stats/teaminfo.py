#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import re
import sys
from statsdb import db_open, db_close, get_teams, get_groups, insert_teams, insert_group
from statsfiles import teaminfo_files
from statsutils import find_value_in_array2args, replace_nonascii, path, send_mail, debug

__author__ = 'fearless'


class TeamHandler(ContentHandler):
    def __init__(self):
        self.parent_id = 0
        self.sport = 0
        self.id = 0
        self.group_id = 0
        self.global_id = 0
        self.city = ''
        self.name = ''
        self.alias = ''
        self.season = ''
        self.conference = ''
        self.division = ''
        self.league_id = ''
        self.league_name = ''
        self.state = ''
        self.country = ''
        self.insertdata = []
        self.teams = []
        self.groups = []

        self.isMLB = True
        self.isLeague = False
        self.isSeason = False
        self.isConference = False
        self.isDivision = False
        self.isTeam = False
        self.isAllStarTeams = False

    def startElement(self, name, attrs):
        if name in ['nfl', 'mlb', 'nba', 'sports-teams', 'nhl', 'wnba', 'wcbk-teams', 'cbk-teams', 'cfb-teams']:
            self.insertdata = []
        elif name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            if self.season is None:
                self.season = attrs.get('year')
            self.teams = get_teams(c, self.league_id)
            self.groups = get_groups(c, self.parent_id)
        elif name == 'conference':
            self.isConference = True
            self.conference = attrs.get('label')
        elif name == 'league':
            self.isLeague = True
            if self.isMLB:
                self.conference = attrs.get('label')
        elif name == 'division':
            self.isDivision = True
            self.division = attrs.get('label')
        elif name == 'team':
            self.isTeam = True
            self.global_id = attrs.get('global-id')
            self.city = attrs.get('city')
            self.name = attrs.get('name')
            self.alias = attrs.get('alias')
        elif name == 'team-info':
            self.isTeam = True
            self.global_id = attrs.get('global-id')
            self.city = attrs.get('name')
            if self.city == '':
                self.city = attrs.get('display-name')
            self.name = attrs.get('nickname')
            if self.name is None:
                self.name = attrs.get('name')
            self.country = attrs.get('country')
            if self.country is None:
                self.country = ''
            if not self.isConference:
                self.conference = attrs.get('conference-name')
                if self.conference is None:
                    self.conference = ''
            if not self.isDivision:
                self.division = attrs.get('division-name')
                if self.division is None:
                    self.division = ''
            self.alias = attrs.get('alias')
        elif name == 'all-star-teams':
            self.isAllStarTeams = True
            self.conference = 'All Star Teams'
        return

    def endElement(self, name):
        if name in ['nfl', 'mlb', 'nba', 'sports-teams', 'nhl', 'cfb-teams', 'cbk-teams', 'wcbk-teams', 'wnba']:
            self.isMLB = False
            data = str.join(',', self.insertdata)
            insert_teams(c, data)
        elif name == 'season':
            self.isSeason = False
        elif name == 'conference':
            self.isConference = False
            self.conference = ''
        elif name == 'league':
            self.isLeague = False
            self.conference = ''
        elif name == 'division':
            self.isDivision = False
            self.division = ''
        elif name == 'all-star-teams':
            self.isAllStarTeams = False
        elif name == 'team' \
                or name == 'team-info':
            self.isTeam = False
            gid = find_value_in_array2args(self.groups, self.global_id)
            if gid is not None:
                self.group_id = int(gid or 0)
            else:
                self.group_id = insert_group(c, conn, self)
            sid = find_value_in_array2args(self.teams, self.global_id)
            if sid is None:
                self.id = 0
            else:
                self.id = int(sid or 0)
            self.insertdata.append("("
                                   + str(self.id) +
                                   ","
                                   + str(self.group_id) +
                                   ","
                                   + str(self.global_id) +
                                   ",'"
                                   + replace_nonascii(self.city) +
                                   "','"
                                   + replace_nonascii(self.name) +
                                   "','"
                                   + re.escape(self.alias) +
                                   "','"
                                   + str(self.season) +
                                   "','"
                                   + re.escape(self.conference) +
                                   "','"
                                   + re.escape(self.division) +
                                   "','"
                                   + str(self.league_id) +
                                   "')")
            self.city = ''
            self.name = ''
            self.alias = ''
            self.state = ''
            self.country = ''


if __name__ == "__main__":
    try:
        cc = db_open()
        c = cc[0]
        conn = cc[1]

        parser = make_parser()
        for file in teaminfo_files:
            if os.path.exists(path + file[2]):
                if debug:
                    print file[2]
                curHandler = TeamHandler()
                curHandler.parent_id = file[0]
                curHandler.sport = file[1]
                curHandler.league_id = file[0]
                curHandler.league_name = file[3]
                parser.setContentHandler(curHandler)
                parser.parse(open(path + file[2]))

        db_close(c, conn)
    except:
        if debug:
            print traceback.format_exc()
        else:
            send_mail(traceback.format_exc())
        sys.exit(1)
