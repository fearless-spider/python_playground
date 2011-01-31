import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
from datetime import datetime, timedelta
import urllib2

screen = 'livescores'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
news = False

yesterday = datetime.today() - timedelta(days=1)


class Boxscore:
    id = 0
    league_id = 0
    competition_id = ''
    start_date = ''
    status = ''
    period = ''
    period_time = ''


class Team:
    team_id = 0
    team_short = ''
    score = 0


def get_league(c, league):
    c.execute("SELECT id FROM wp_bp_leagues WHERE short = '%s'" % league)
    return c.fetchone()


def get_team_by_feedid(c, feedid):
    c.execute("SELECT id,short FROM wp_bp_teams WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_score(c, data):
    c.execute("SELECT * FROM wp_bp_teams_boxscores WHERE competition_id = '%s'" % (data.competition_id))
    return c.fetchone()


def insert_score(c, data, home, away):
    if data.id:
        sql = "UPDATE wp_bp_teams_boxscores SET `league_id` = %d,`start_date` = '%s',`status` = '%s',`period` = '%s',`period_time` = '%s',`competition_id` = '%s',`home_team_short` = '%s',`home_team_id` = %d, `home_score` = %d,`away_team_short` = '%s',`away_team_id` = %d, `away_score` = %d WHERE id = %d;" % (
        data.league_id, data.start_date, data.status, data.period, data.period_time, data.competition_id,
        home.team_short, home.team_id, home.score, away.team_short, away.team_id, away.score, data.id)
    else:
        sql = "INSERT INTO wp_bp_teams_boxscores(`league_id`,`start_date`,`status`,`period`,`period_time`,`competition_id`,`home_team_short`,`home_team_id`,`home_score`,`away_team_short`,`away_team_id`,`away_score`) VALUES (%d,'%s','%s','%s','%s','%s','%s',%d,%d,'%s',%d,%d);" % (
        data.league_id, data.start_date, data.status, data.period, data.period_time, data.competition_id,
        home.team_short, home.team_id, home.score, away.team_short, away.team_id, away.score)
    print sql
    c.execute(sql)


try:
    conn = MySQLdb.connect("localhost", "", "", "")

    c = conn.cursor()

    d = feedparser.parse(
        "http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + yesterday.strftime(
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
            lid = get_league(c, league)
            league_id = int(lid[0])
            for xcompetition in soup.findAll('competition'):
                boxscore = Boxscore()
                boxscore.league_id = league_id
                for xid in xcompetition.findAll('id'):
                    boxscore.competition_id = xid.string
                    break
                for status in xcompetition.findAll('competition-status'):
                    boxscore.status = status.contents[0].string
                for start_date in xcompetition.findAll('start-date'):
                    start_date = start_date.contents[0].string
                    boxscore.start_date = start_date[0:start_date.find('T')] + ' ' + start_date[start_date.find(
                        'T') + 1:start_date.find('T') + 5 + start_date.find('-')]
                for scope in xcompetition.findAll('scope'):
                    num = str(scope.get('num'))
                    type = str(scope.get('type'))
                    sub_type = str(scope.get('sub-type'))
                    if type == 'inning':
                        if num == '1':
                            num = num + 'st'
                        elif num == '2':
                            num = num + 'nd'
                        elif num == '3':
                            num = num + 'rd'
                        else:
                            num = num + 'th'
                        boxscore.period = (sub_type + ' ' + num).upper()
                    else:
                        boxscore.period = (num + ' ' + type).upper()
                for clock in xcompetition.findAll('clock'):
                    boxscore.period_time = clock.string
                for xteam in xcompetition.findAll('home-team-content'):
                    home = Team()
                    for team in xteam.findAll('team'):
                        for id in team.findAll('id'):
                            feedid = id.string
                        tid = get_team_by_feedid(c, feedid)
                        if tid is None:
                            break
                        home.team_id = int(tid[0])
                        home.team_short = tid[1]
                    for xscope in xteam.findAll('stat-group'):
                        for xstat in xscope.findAll('stat'):
                            if str(xstat.get('type')) == 'points' or str(xstat.get('type')) == 'runs' or str(
                                    xstat.get('type')) == 'goals':
                                home.score = int(xstat.get('num'))
                        break

                for xteam in xcompetition.findAll('away-team-content'):
                    away = Team()
                    for team in xteam.findAll('team'):
                        for id in team.findAll('id'):
                            feedid = id.string
                        tid = get_team_by_feedid(c, feedid)
                        if tid is None:
                            break
                        away.team_id = int(tid[0])
                        away.team_short = tid[1]
                    for xscope in xteam.findAll('stat-group'):
                        for xstat in xscope.findAll('stat'):
                            if str(xstat.get('type')) == 'points' or str(xstat.get('type')) == 'runs' or str(
                                    xstat.get('type')) == 'goals':
                                away.score = int(xstat.get('num'))
                        break

                sid = get_score(c, boxscore)
                if sid is not None:
                    boxscore.id = int(sid[0])
                insert_score(c, boxscore, home, away)

            page.close()
    conn.commit()
    c.close()
    conn.close()
except MySQLdb.Error, e:
    print "Guru Meditation #%d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
