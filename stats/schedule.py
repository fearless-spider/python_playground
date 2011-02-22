#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import sys
from statsfiles import schedule_files
from statsutils import replace_nonascii, slugfy, find_value_in_array2args, path, send_mail, debug
from statsdb import get_teams_group, get_event, insert_events, db_open

__author__ = 'fearless'


class NBAHandler(ContentHandler):
    def __init__(self):
        self.away_name = ''
        self.away_city = ''
        self.home_name = ''
        self.home_city = ''
        self.id = 0
        self.name = ''
        self.type = ''
        self.description = ''
        self.country = ''
        self.state = ''
        self.city = ''
        self.address = ''
        self.note = ''
        self.startdate = ''
        self.enddate = ''
        self.starthour = ''
        self.endhour = ''
        self.startmin = ''
        self.endmin = ''
        self.startunix = ''
        self.endunix = ''
        self.grouplink = 0
        self.grouplinkvs = 0
        self.season = ''
        self.global_id = 0
        self.insertdata = []
        self.teams = []

        self.schedule_name = ['nba-schedule', 'wnba-schedule', 'basketball-cbk-schedule', 'basketball-wcbk-schedule',
                              'hockey-nhl-schedule', 'soccer-ifb-schedule', 'football-cfb-schedule',
                              'football-nfl-schedule', 'baseball-mlb-schedule']
        self.isSeason = False
        self.isNBASchedule = False
        self.isGameSchedule = False
        self.isHome = False
        self.isAway = False

    def startElement(self, name, attrs):
        if name == 'season':
            self.isSeason = True
            self.season = attrs.get('season')
            if self.season is None:
                self.season = attrs.get('year')
            self.teams = get_teams_group(c, str(league_id))
        elif name in self.schedule_name:
            self.isNBASchedule = True
            self.insertdata = []
        elif name == 'game-schedule':
            self.isGameSchedule = True
            self.id = 0
            self.name = ''
            self.type = ''
            self.description = ''
            self.country = ''
            self.state = ''
            self.city = ''
            self.address = ''
            self.note = ''
            self.date = ''
            self.time = ''
            self.enddate = ''
            self.starthour = ''
            self.endhour = ''
            self.startmin = ''
            self.endmin = ''
            self.startunix = ''
            self.endunix = ''
            self.grouplink = 0
            self.grouplinkvs = 0
            self.global_id = ''
            self.away_name = ''
            self.home_name = ''
            self.away_city = ''
            self.home_city = ''
        elif name == 'visiting-team':
            self.isAway = True
        elif name == 'home-team':
            self.isHome = True
        elif name == 'gametype':
            self.type = attrs.get('type')
        elif name == 'game-type':
            self.type = attrs.get('description')
        elif name == 'gamecode':
            self.global_id = attrs.get('global-id')
            if self.global_id is None:
                self.global_id = attrs.get('global-code')
        elif name == 'date' and self.isGameSchedule:
            self.date = attrs.get('year') + '-' + attrs.get('month') + '-' + attrs.get('date')
        elif name == 'time' and self.isGameSchedule:
            self.starthour = attrs.get('hour')
            if self.starthour == '':
                self.starthour = "00"
            self.endhour = attrs.get('hour')
            if self.endhour == '':
                self.endhour = "00"
            self.startmin = attrs.get('minute')
            if self.startmin == '':
                self.startmin = "00"
            self.endmin = attrs.get('minute')
            if self.endmin == '':
                self.endmin = "00"
            self.time = self.starthour + ':' + self.startmin + ':00'
        elif name == 'team-code':
            if self.isAway:
                self.grouplink = int(find_value_in_array2args(self.teams, attrs.get('global-id')) or 0)
            else:
                self.grouplinkvs = int(find_value_in_array2args(self.teams, attrs.get('global-id')) or 0)
        elif name == 'team-name':
            if self.isAway:
                self.away_name = attrs.get('name')
            else:
                self.home_name = attrs.get('name')
        elif name == 'team-city':
            if self.isAway:
                self.away_city = attrs.get('city')
            else:
                self.home_city = attrs.get('city')
        elif name == 'team-info':
            if self.isAway:
                self.grouplink = int(find_value_in_array2args(self.teams, attrs.get('global-id')) or 0)
                self.away_name = attrs.get('display-name')
            else:
                self.grouplinkvs = int(find_value_in_array2args(self.teams, attrs.get('global-id')) or 0)
                self.home_name = attrs.get('display-name')
        elif name == 'station':
            self.note = attrs.get('name')
            if self.note is None:
                self.note = ''
            else:
                self.note = self.note
        elif name == 'stadium':
            self.description = attrs.get('name')
            if self.description is None:
                self.description = ''
            else:
                self.description = self.description
            self.city = attrs.get('city')
            if self.city is None:
                self.city = ''
            else:
                self.city = self.city
            self.state = attrs.get('state')
            if self.state is None:
                self.state = ''
            self.country = attrs.get('country')
            if self.country is None:
                self.country = ''

        return

    def endElement(self, name):
        if name == 'season':
            self.isSeason = False
        elif name == 'visiting-team':
            self.isAway = False
        elif name == 'home-team':
            self.isHome = False
        elif name in self.schedule_name:
            self.isNBASchedule = False
        elif name == 'game-schedule' and self.grouplink != 0 and self.grouplinkvs != 0:
            self.isGameSchedule = False
            cid = get_event(c, self.global_id)
            if cid is not None:
                self.id = int(cid[0] or 0)
            else:
                self.id = 0
            if self.away_city != '':
                name = replace_nonascii(self.away_city) + " " + replace_nonascii(
                    self.away_name) + " at " + replace_nonascii(self.home_city) + " " + replace_nonascii(self.home_name)
            else:
                name = replace_nonascii(self.away_name) + " at " + replace_nonascii(self.home_name)
            d = time.strptime(self.date + ' ' + self.time, "%Y-%m-%d %H:%M:%S")
            self.insertdata.append("("
                                   + str(self.id) +
                                   ",1,'"
                                   + name +
                                   "','"
                                   + str(self.type) +
                                   "',1,'"
                                   + slugfy(
                replace_nonascii(self.away_name) + ' at ' + replace_nonascii(self.home_name) + ' ' + self.date, '-') +
                                   "','"
                                   + replace_nonascii(self.description) +
                                   "','','"
                                   + replace_nonascii(self.country) +
                                   "','"
                                   + replace_nonascii(self.state) +
                                   "','"
                                   + replace_nonascii(self.city) +
                                   "','"
                                   + str(self.address) +
                                   "','"
                                   + replace_nonascii(self.note) +
                                   "','','','','','"
                                   + datetime.fromtimestamp(time.mktime(d)).strftime("%d/%m/%Y") +
                                   "','"
                                   + datetime.fromtimestamp(time.mktime(d)).strftime("%d/%m/%Y") +
                                   "','"
                                   + str(self.starthour) +
                                   "','"
                                   + str(self.endhour) +
                                   "','"
                                   + str(self.startmin) +
                                   "','"
                                   + str(self.endmin) +
                                   "','"
                                   + str(time.mktime(d))[0:10] +
                                   "','"
                                   + str(time.mktime(d))[0:10] +
                                   "','public',"
                                   + str(self.grouplink) +
                                   ","
                                   + str(self.grouplinkvs) +
                                   ",1,1,0,'"
                                   + self.date + " " + self.time +
                                   "','','"
                                   + str(self.season) +
                                   "','"
                                   + self.global_id +
                                   "','"
                                   + league_name +
                                   "')")
            data = str.join(',', self.insertdata)
            # print data
            insert_events(c, conn, data, self.id)
            self.insertdata = []


if __name__ == "__main__":
    try:
        cc = db_open()
        c = cc[0]
        conn = cc[1]

        parser = make_parser()
        for file in schedule_files:
            if os.path.exists(path + file[1]):
                print file[1]
                league_id = file[0]
                league_name = file[2]
                curHandler = NBAHandler()
                parser.setContentHandler(curHandler)
                parser.parse(open(path + file[1]))

        conn.commit()
        c.close()
        conn.close()
    except:
        if debug:
            print traceback.format_exc()
        else:
            send_mail(traceback.format_exc())
        sys.exit(1)
