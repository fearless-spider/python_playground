# -*- coding: utf-8 -*-
import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
from datetime import datetime, timedelta
import urllib2

screen = 'standings'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
news = False


class Season:
    id = 0
    feed_id = ''
    name = ''
    stardate = ''
    enddate = ''
    league_id = 0


class Standings:
    id = 0
    team_id = 0
    conference_feed_id = ''
    division_feed_id = ''
    team_feed_id = ''
    won = 0
    lost = 0
    draw = 0
    pts = 0
    gls = 0
    glo = 0
    otl = 0
    lrank = 0
    drank = 0
    gb = 0
    '''home'''
    hwon = 0
    hlost = 0
    hshot = 0
    hover = 0
    hdraw = 0
    home = ''
    '''road'''
    rwon = 0
    rlost = 0
    rshot = 0
    rover = 0
    rdraw = 0
    road = ''
    '''division'''
    dwon = 0
    dlost = 0
    div = ''
    '''conference'''
    cwon = 0
    clost = 0
    conf = ''
    '''l10'''
    l10won = 0
    l10lost = 0
    l10 = ''
    '''pa and pf'''
    pf = 0
    rf = 0
    pa = 0
    ra = 0
    gf = 0
    ga = 0
    diff = 0
    slost = 0
    swon = 0
    streak = ''


def get_team_by_feedid(c, feedid):
    c.execute("SELECT id FROM wp_bp_teams WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_stand(c, season_feed_id, team_id):
    c.execute("SELECT id FROM standings WHERE season_feed_id = '%s' AND team_id = %d" % (season_feed_id, team_id))
    return c.fetchone()


def insert_standing(c, data):
    if (data != ''):
        sql = """INSERT INTO standings(
        `id`,
        `won`,
        `lost`,
        `conf`,
        `div`,
        `home`,
        `road`,
        `l10`,
        `streak`,
        `otl`,
        `gb`,
        `pf`,
        `pa`,
        `rf`,
        `ra`,
        `gf`,
        `ga`,
        `diff`,
        `team_id`,
        `team_feed_id`,
        `conference_ranking`,
        `division_ranking`,
        `conference_feed_id`,
        `division_feed_id`,
        `season_feed_id`,
        `pts`,
        `draw`
        ) VALUES %s 
        ON DUPLICATE KEY UPDATE 
        `won` = VALUES(`won`),
        `lost` = VALUES(`lost`),
        `conf` = VALUES(`conf`),
        `div` = VALUES(`div`),
        `home` = VALUES(`home`),
        `road` = VALUES(`road`),
        `l10` = VALUES(`l10`),
        `streak` = VALUES(`streak`),
        `otl` = VALUES(`otl`),
        `gb` = VALUES(`gb`),
        `pf` = VALUES(`pf`),
        `pa` = VALUES(`pa`),
        `rf` = VALUES(`rf`),
        `ra` = VALUES(`ra`),
        `gf` = VALUES(`gf`),
        `ga` = VALUES(`ga`),
        `diff` = VALUES(`diff`),
        `conference_ranking` = VALUES(`conference_ranking`),
        `division_ranking` = VALUES(`division_ranking`),
        `pts` = VALUES(`pts`),
        `draw` = VALUES(`draw`)
        ;""" % data
        #        print sql
        c.execute(sql)


def get_season(c, feedid):
    c.execute("SELECT id FROM wp_bp_seasons WHERE feed_id = '%s'" % feedid)
    return c.fetchone()


def insert_season(c, data):
    sql = "INSERT INTO wp_bp_seasons(feed_id,name,startdate,enddate,league_id) VALUES ('%s','%s','%s','%s',%d);" % (
    data.feed_id, conn.escape_string(data.name), data.startdate, data.enddate, data.league_id)
    c.execute(sql)


def get_league(c, league):
    c.execute("SELECT id FROM wp_bp_leagues WHERE short = '%s'" % league)
    return c.fetchone()


def prepare_data(division, con=False):
    insertdata = []
    index = 0
    if league == 'MLB' or league == 'NBA':
        for stand in division:
            if con:
                if stand.lrank == 1:
                    break
            else:
                if stand.drank == 1:
                    break

            index += 1
        first = division[index]
    stand = Standings()

    for stand in division:
        wl = float(stand.won + stand.lost)
        if wl == 0.0:
            wl = 1.0
        '''PTS'''
        if league == 'MLS':
            stand.pts = (stand.won * 3) + stand.draw
        '''OTL'''
        if league == 'NHL':
            stand.otl = stand.glo + stand.gls
        else:
            stand.otl = stand.won / wl
        '''GB'''
        if league == 'MLB' or league == 'NBA':
            stand.gb = ((first.won - stand.won) + (stand.lost - first.lost)) / 2.0
        '''HOME'''
        if stand.hover or stand.hshot:
            stand.home = str(stand.hwon) + ' - ' + str(stand.hlost) + ' - ' + str(stand.hover + stand.hshot)
        else:
            stand.home = str(stand.hwon) + ' - ' + str(stand.hlost)
        if league == 'MLS':
            stand.home = str(stand.hwon) + ' - ' + str(stand.hlost) + ' - ' + str(stand.hdraw)
        '''ROAD'''
        if stand.rover or stand.rshot:
            stand.road = str(stand.rwon) + ' - ' + str(stand.rlost) + ' - ' + str(stand.rover + stand.rshot)
        else:
            stand.road = str(stand.rwon) + ' - ' + str(stand.rlost)
        if league == 'MLS':
            stand.road = str(stand.rwon) + ' - ' + str(stand.rlost) + ' - ' + str(stand.rdraw)
        if league != 'MLS':
            '''DIV'''
            stand.div = str(stand.dwon) + ' - ' + str(stand.dlost)
            '''CONF'''
            stand.conf = str(stand.cwon) + ' - ' + str(stand.clost)
            '''L10'''
            stand.l10 = str(stand.l10won) + ' - ' + str(stand.l10lost)
        if league == 'NCAA BB' or league == 'NBA':
            stand.pf = stand.pf / wl
            stand.pa = stand.pa / wl
            stand.diff = stand.pf - stand.pa
        if league == 'MLB':
            stand.diff = stand.rf - stand.ra
        if league == 'MLS' or league == 'NHL':
            stand.diff = stand.gf - stand.ga
        if league == 'NCAA FB' or league == 'NFL':
            stand.diff = stand.pf - stand.pa
        if stand.slost > stand.swon:
            stand.streak = 'Lost ' + str(stand.slost)
        else:
            stand.streak = 'Won ' + str(stand.swon)
        insertdata.append("("
                          + str(stand.id) +
                          ","
                          + str(stand.won) +
                          ","
                          + str(stand.lost) +
                          ",'"
                          + str(stand.conf) +
                          "','"
                          + str(stand.div) +
                          "','"
                          + str(stand.home) +
                          "','"
                          + str(stand.road) +
                          "','"
                          + str(stand.l10) +
                          "','"
                          + str(stand.streak) +
                          "',"
                          + str(stand.otl) +
                          ","
                          + str(stand.gb) +
                          ","
                          + str(stand.pf) +
                          ","
                          + str(stand.pa) +
                          ","
                          + str(stand.rf) +
                          ","
                          + str(stand.ra) +
                          ","
                          + str(stand.gf) +
                          ","
                          + str(stand.ga) +
                          ","
                          + str(stand.diff) +
                          ","
                          + str(stand.team_id) +
                          ",'"
                          + str(stand.team_feed_id) +
                          "',"
                          + str(stand.lrank) +
                          ","
                          + str(stand.drank) +
                          ",'"
                          + str(stand.conference_feed_id) +
                          "','"
                          + str(stand.division_feed_id) +
                          "','"
                          + str(stand.season_feed_id) +
                          "',"
                          + str(stand.pts) +
                          ","
                          + str(stand.draw) +
                          ")")
    return insertdata


def prepare_division(xdivisioncontent, season_feed_id, conference_feed_id, division_feed_id):
    for xteamcontent in xdivisioncontent.findAll('team-content'):
        team_feed_id = xteamcontent.contents[0].contents[0].string
        tid = get_team_by_feedid(c, team_feed_id)
        if tid is None:
            break
        team_id = int(tid[0] or 0)
        data = Standings()
        sid = get_stand(c, season_feed_id, team_id)
        if sid is not None:
            data.id = int(sid[0] or 0)
        for xstatgroup in xteamcontent.findAll('stat-group'):
            for xstat in xstatgroup.findAll('stat'):
                group = xstatgroup.contents[0].string
                type = xstat.get('type')
                num = float(xstat.get('num') or 0)
                if (group == 'league-standings' and type == 'games_won'):
                    data.won = int(num or 0)
                if (group == 'league-standings' and type == 'games_lost'):
                    data.lost = int(num or 0)
                if (group == 'league-standings' and type == 'games_tied' and league == 'MLS'):
                    data.draw = int(num or 0)
                if (group == 'league-standings' and type == 'games_lost_shootout' and league == 'NHL'):
                    data.gls = int(num or 0)
                if (group == 'league-standings' and type == 'games_lost_overtime' and league == 'NHL'):
                    data.glo = int(num or 0)
                if (group == 'division-standings' and type == 'division_ranking'):
                    data.drank = int(num or 0)
                if (group == 'conference-standings' and type == 'conference_ranking'):
                    data.lrank = int(num or 0)
                if (group == 'home-league-standings' and type == 'games_won'):
                    data.hwon = int(num or 0)
                if (group == 'home-league-standings' and type == 'games_lost'):
                    data.hlost = int(num or 0)
                if (group == 'home-league-standings' and type == 'games_lost_shootout'):
                    data.hshot = int(num or 0)
                if (group == 'home-league-standings' and type == 'games_lost_overtime'):
                    data.hover = int(num or 0)
                if (group == 'home-league-standings' and type == 'games_tied' and league == 'MLS'):
                    data.hdraw = int(num or 0)
                if (group == 'away-league-standings' and type == 'games_won'):
                    data.rwon = int(num or 0)
                if (group == 'away-league-standings' and type == 'games_lost'):
                    data.rlost = int(num or 0)
                if (group == 'away-league-standings' and type == 'games_lost_shootout'):
                    data.rshot = int(num or 0)
                if (group == 'away-league-standings' and type == 'games_lost_overtime'):
                    data.rover = int(num or 0)
                if (group == 'away-league-standings' and type == 'games_tied' and league == 'MLS'):
                    data.rdraw = int(num or 0)
                if (group == 'conference-standings' and type == 'games_won' and league != 'MLS'):
                    data.cwon = int(num or 0)
                if (group == 'conference-standings' and type == 'games_lost' and league != 'MLS'):
                    data.clost = int(num or 0)
                if (group == 'division-standings' and type == 'games_won' and league != 'MLS'):
                    data.dwon = int(num or 0)
                if (group == 'division-standings' and type == 'games_lost' and league != 'MLS'):
                    data.dlost = int(num or 0)
                if (group == 'last-10-league-standings' and type == 'games_won' and league != 'MLS'):
                    data.l10won = int(num or 0)
                if (group == 'last-10-league-standings' and type == 'games_lost' and league != 'MLS'):
                    data.l10lost = int(num or 0)
                if (group == 'league-standings' and type == 'points_for' and (
                        league == 'NCAA BB' or league == 'NBA' or league == 'NCAA FB' or league == 'NFL')):
                    data.pf = float(num or 0)
                if (group == 'league-standings' and type == 'points_against' and (
                        league == 'NCAA BB' or league == 'NBA' or league == 'NCAA FB' or league == 'NFL')):
                    data.pa = float(num or 0)
                if (group == 'league-standings' and type == 'runs_for' and league == 'MLB'):
                    data.rf = int(num or 0)
                if (group == 'league-standings' and type == 'runs_against' and league == 'MLB'):
                    data.ra = int(num or 0)
                if (group == 'league-standings' and type == 'goals_for' and league == 'NHL'):
                    data.gf = int(num or 0)
                if (group == 'league-standings' and type == 'goals_against' and league == 'NHL'):
                    data.ga = int(num or 0)
                if (group == 'league-standings' and type == 'goals' and league == 'MLS'):
                    data.gf = int(num or 0)
                if (group == 'league-standings' and type == 'goals_against' and league == 'MLS'):
                    data.ga = int(num or 0)
                if (group == 'league-standings' and type == 'loss_streak'):
                    data.slost = int(num or 0)
                if (group == 'league-standings' and type == 'win_streak'):
                    data.swon = int(num or 0)
        data.team_id = team_id
        data.season_feed_id = season_feed_id
        data.conference_feed_id = conference_feed_id
        data.division_feed_id = division_feed_id
        data.team_feed_id = team_feed_id
    return data


# Calculating the current datetime minus 1 day
d = datetime.today() - timedelta(days=1)

try:
    conn = MySQLdb.connect("localhost", "", "", "")

    c = conn.cursor()

    if len(sys.argv) == 5:
        season = sys.argv[4]
        d = feedparser.parse("http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "/" + season)
    else:
        d = feedparser.parse(
            "http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + d.strftime(
                "%Y-%m-%dT%H:%M:%S"))

    items = []

    if len(d['entries']):
        for item in d.entries:
            if (item.link.find('/' + direct + '/') > 0):
                if (item.link.find('/' + str(news) + '/') > 0 and news != False):
                    items.append(str(item.link))
                else:
                    items.append(str(item.link))
        items.reverse()
        for item in items:
            page = urllib2.urlopen(item)
            soup = BeautifulStoneSoup(page)
            for xseason in soup.findAll('season'):
                season = Season()
                season.feed_id = xseason.contents[0].string
                season.name = xseason.contents[1].string
                season.startdate = xseason.contents[2].contents[0].string
                season.enddate = xseason.contents[2].contents[1].string
                lid = get_league(c, league)
                season.league_id = lid[0]
                sid = get_season(c, season.feed_id)
                if sid is None:
                    insert_season(c, season)  # insert season
                    season_id = conn.insert_id()
                else:
                    season_id = sid[0]
                season_feed_id = season.feed_id
            for xconferencecontent in soup.findAll('conference-content'):
                conference_feed_id = xconferencecontent.contents[0].contents[0].string
                division_feed_id = ''
                xdiv = xconferencecontent.findAll('division-content')
                if len(xdiv):
                    for xdivisioncontent in xdiv:
                        division_feed_id = xdivisioncontent.contents[0].contents[0].string
                        division = []
                        division.append(
                            prepare_division(xdivisioncontent, season_feed_id, conference_feed_id, division_feed_id))
                        data = str.join(',', prepare_data(division))
                        insert_standing(c, data)
                else:
                    division = []
                    division.append(
                        prepare_division(xconferencecontent, season_feed_id, conference_feed_id, division_feed_id))
                    data = str.join(',', prepare_data(division, True))
                    insert_standing(c, data)

            page.close()
    conn.commit()
    c.close()
    conn.close()
except MySQLdb.Error, e:
    print "Guru Meditation #%d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
