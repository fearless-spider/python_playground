import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
from datetime import date, timedelta
import urllib2

screen = 'standings'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
# season = sys.argv[4]
news = False


class Season:
    id = 0
    feed_id = ''
    name = ''
    stardate = ''
    enddate = ''
    league_id = 0


class Stand:
    id = 0
    season_feed_id = ''
    conference_feed_id = ''
    division_feed_id = ''
    team_feed_id = ''
    team_id = 0
    group = ''
    type = ''
    num = 0


conn = MySQLdb.connect("localhost", "", "", "")

c = conn.cursor()


def get_team_by_feedid(c, feedid):
    c.execute("SELECT id FROM wp_bp_teams WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_stand(c, data):
    c.execute(
        "SELECT id FROM wp_bp_teams_standings WHERE `group` = '%s' AND `type` = '%s' AND season_feed_id = '%s' AND team_id = %d" % (
        data.group, data.type, data.season_feed_id, data.team_id))
    return c.fetchone()


def insert_standing(c, data):
    if data.id:
        sql = "UPDATE wp_bp_teams_standings SET `group` = '%s',`type` = '%s',`num` = %f,`team_id` = %d,`season_feed_id` = '%s',`conference_feed_id` = '%s',`division_feed_id` = '%s',`team_feed_id` = '%s' WHERE id = %d;" % (
        data.group, data.type, data.num, data.team_id, data.season_feed_id, data.conference_feed_id,
        data.division_feed_id, data.team_feed_id, data.id)
    else:
        sql = "INSERT INTO wp_bp_teams_standings(`group`,`type`,`num`,`team_id`,`season_feed_id`,`conference_feed_id`,`division_feed_id`,`team_feed_id`) VALUES ('%s','%s',%f,%d,'%s','%s','%s','%s');" % (
        data.group, data.type, data.num, data.team_id, data.season_feed_id, data.conference_feed_id,
        data.division_feed_id, data.team_feed_id)
    print sql
    c.execute(sql)


def get_season(c, feedid):
    c.execute("SELECT id FROM wp_bp_seasons WHERE feed_id = '%s'" % feedid)
    return c.fetchone()


def insert_season(c, data):
    sql = "INSERT INTO wp_bp_seasons(feed_id,name,startdate,enddate,league_id) VALUES ('%s','%s','%s','%s',%d);" % (
    data.feed_id, conn.escape_string(data.name), data.startdate, data.enddate, data.league_id)
    print sql
    c.execute(sql)


def get_league(c, league):
    c.execute("SELECT id FROM wp_bp_leagues WHERE short = '%s'" % league)
    return c.fetchone()


# Calculating the current datetime minus 1 day
from datetime import datetime, timedelta

d = datetime.today() - timedelta(days=1)

# d = feedparser.parse("http://xml.sportsdirectinc.com/Atom?feed=/"+sport+"/"+screen+"/"+season)
d = feedparser.parse("http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + d.strftime(
    "%Y-%m-%dT%H:%M:%S"))

items = []
insertdata = []

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
            for xdivisioncontent in xconferencecontent.findAll('division-content'):
                division_feed_id = xdivisioncontent.contents[0].contents[0].string
            for xteamcontent in xconferencecontent.findAll('team-content'):
                team_feed_id = xteamcontent.contents[0].contents[0].string
                tid = get_team_by_feedid(c, team_feed_id)
                if tid is None:
                    break
                team_id = int(tid[0] or 0)
                for xstatgroup in xteamcontent.findAll('stat-group'):
                    for xstat in xstatgroup.findAll('stat'):
                        data = Stand()
                        data.group = xstatgroup.contents[0].string
                        data.type = xstat.get('type')
                        data.num = float(xstat.get('num') or 0)
                        data.team_id = team_id
                        data.season_feed_id = season_feed_id
                        data.conference_feed_id = conference_feed_id
                        data.division_feed_id = division_feed_id
                        data.team_feed_id = team_feed_id
                        id = get_stand(c, data)
                        if id is not None:
                            data.id = id[0]
                        insert_standing(c, data)
        page.close()
conn.commit()
