import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
from datetime import date, timedelta
import urllib2

screen = 'players'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
# season = sys.argv[4]

news = False


class Player:
    id = 0
    feed_id = ''
    firstname = ''
    lastname = ''
    height = 0
    weight = 0
    city = ''
    state = ''
    country = ''
    birthdate = ''
    active = 1
    number = 0
    position = ''
    salary = ''
    team_id = 0


conn = MySQLdb.connect("localhost", "", "", "")

c = conn.cursor()


def get_conference_by_league(c, league, season_name):
    c.execute(
        "SELECT c.* FROM wp_bp_conferences AS c LEFT JOIN wp_bp_seasons AS s ON c.season_id = s.id LEFT JOIN wp_bp_leagues AS l ON s.league_id = l.id WHERE l.short = '%s' AND s.name = '%s'" % (
        league, season_name))
    return c.fetchall()


def get_team_by_feedid(c, feedid):
    c.execute("SELECT id FROM wp_bp_teams WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_player(c, feed_id):
    c.execute("SELECT id FROM wp_bp_teams_players WHERE feed_id = '%s'" % (feed_id))
    return c.fetchone()


def insert_player(c, data):
    if (data.id):
        sql = "UPDATE wp_bp_teams_players SET feed_id = '%s',firstname = '%s',lastname = '%s',team_id = %d,height = %d,weight = %d,birthdate = '%s',city = '%s',state = '%s',country = '%s',number = %d,position = '%s',active = %d,salary = '%s' WHERE id = %d ;" % (
        data.feed_id, conn.escape_string(data.firstname), conn.escape_string(data.lastname), data.team_id, data.height,
        data.weight, conn.escape_string(data.birthdate), conn.escape_string(data.city), conn.escape_string(data.state),
        conn.escape_string(data.country), data.number, conn.escape_string(data.position), data.active,
        conn.escape_string(data.salary), data.id)
    else:
        sql = "INSERT INTO wp_bp_teams_players(feed_id,firstname,lastname,team_id,height,weight,birthdate,city,state,country,number,position,active,salary) VALUES ('%s','%s','%s','%d','%d','%d','%s','%s','%s','%s','%d','%s','%d','%s');" % (
        data.feed_id, conn.escape_string(data.firstname), conn.escape_string(data.lastname), data.team_id, data.height,
        data.weight, conn.escape_string(data.birthdate), conn.escape_string(data.city), conn.escape_string(data.state),
        conn.escape_string(data.country), data.number, conn.escape_string(data.position), data.active,
        conn.escape_string(data.salary))
        print sql
    c.execute(sql)


def removeNonAscii(s): return "".join(i for i in s if ord(i) < 128)


d = feedparser.parse("http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + (
            date.today() - timedelta(days=1)).isoformat() + "T12:42:13")
# d = feedparser.parse("http://xml.sportsdirectinc.com/Atom?feed=/"+sport+"/"+screen+"/"+season)

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
        for xteam in soup.findAll('team-content'):
            feedid = xteam.contents[0].contents[0].string
            # for conference in get_conference_by_league(c,league,season_name):
            tid = get_team_by_feedid(c, feedid)
            if tid is None:
                continue
            team_id = tid[0]
            for xplayer in xteam.findAll('player'):
                player = Player()
                player.feed_id = xplayer.contents[0].string
                player.firstname = str(removeNonAscii(xplayer.contents[1].string)).encode("ascii", "ignore").encode(
                    "iso-8859-1", "ignore").decode("utf-8", "ignore")
                lastname = xplayer.contents[2].string
                if lastname is not None:
                    player.lastname = str(removeNonAscii(lastname)).encode("ascii", "ignore").encode("iso-8859-1",
                                                                                                     "ignore").decode(
                        "utf-8", "ignore")
                for height in xplayer.findAll('height'):
                    player.height = int(height.contents[0].string)
                for weight in xplayer.findAll('weight'):
                    player.weight = int(weight.contents[0].string)
                for city in xplayer.findAll('city'):
                    player.city = city.contents[0].string.encode("ascii", "ignore").encode("iso-8859-1",
                                                                                           "ignore").decode("utf-8",
                                                                                                            "ignore")
                for state in xplayer.findAll('state'):
                    player.state = state.contents[0].string
                for country in xplayer.findAll('country'):
                    player.country = country.contents[0].string.encode("ascii", "ignore").encode("iso-8859-1",
                                                                                                 "ignore").decode(
                        "utf-8", "ignore")
                for birthdate in xplayer.findAll('birthdate'):
                    player.birthdate = birthdate.contents[0].string
                for active in xplayer.findAll('active'):
                    if active.contents[0].string == 'False':
                        player.active = 0
                    else:
                        player.active = 1
                for number in xplayer.findAll('number'):
                    player.number = int(number.contents[0].string)
                for position in xplayer.findAll('position'):
                    position = position.contents[0].string
                    player.position = position[position.find(':') + 1:]
                for salary in xplayer.findAll('salary'):
                    player.salary = salary.contents[0].string + str(salary.get('currency'))
                player.team_id = team_id;
                player_id = get_player(c, player.feed_id)
                if player_id is not None:
                    player.id = player_id[0]

                insert_player(c, player)

        page.close()

conn.commit()
