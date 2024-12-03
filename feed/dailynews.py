import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
from datetime import date, timedelta
import urllib2

screen = 'news'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
news = False
newstime = (date.today() - timedelta(days=1)).isoformat()


class Article:
    id = 0
    author = ''
    language = ''
    league_id = 0
    title = ''
    source = ''
    date = ''
    body = ''
    team_id = 0


def get_league(c, league):
    c.execute("SELECT id FROM wp_bp_leagues WHERE short = '%s'" % league)
    return c.fetchone()


def get_conference_by_league(c, league):
    c.execute(
        "SELECT c.* FROM wp_bp_conferences AS c LEFT JOIN wp_bp_seasons AS s ON c.season_id = s.id LEFT JOIN wp_bp_leagues AS l ON s.league_id = l.id WHERE l.short = '%s'" % league)
    return c.fetchall()


def get_team_by_feedid(c, feedid):
    c.execute("SELECT id FROM wp_bp_teams WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_dailynews(c, title, team_id):
    c.execute(
        "SELECT id FROM wp_bp_breakingnews WHERE title = '%s' AND team_id = %d" % (conn.escape_string(title), team_id))
    return c.fetchone()


def get_breakingnews(c, title, league_id):
    c.execute("SELECT id FROM wp_bp_breakingnews WHERE title = '%s' AND league_id = %d" % (
    conn.escape_string(title), league_id))
    return c.fetchone()


def insert_dailynews(c, data):
    #    if(data.id == 0):
    #        sql = "UPDATE wp_bp_breakingnews SET title = '%s',source = '%s',team_id = %d,date = '%s',body = '%s' WHERE id = %d ;" % (conn.escape_string(data.title),conn.escape_string(data.source),data.team_id,data.date,conn.escape_string(data.body),data.id)
    #    else:
    if (data != ''):
        sql = "INSERT INTO wp_bp_breakingnews(author,language,league_id,title,source,team_id,date,body) VALUES %s " % data
        #        print sql
        c.execute(sql)


try:
    conn = MySQLdb.connect("localhost", "", "", "")

    c = conn.cursor()

    d = feedparser.parse(
        "http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + newstime + "T12:42:13")

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
            for xarticle in soup.findAll('article'):
                article = Article()
                for team in xarticle.findAll('team'):
                    feedid = team.contents[1].string
                    # for conference in get_conference_by_league(c,league):
                    tid = get_team_by_feedid(c, feedid)
                    # if tid:
                    article.team_id = tid[0]
                for title in xarticle.findAll('title'):
                    article.title = title.contents[0].string.encode("iso-8859-1", "ignore").decode("utf-8", "ignore")
                for source in xarticle.findAll('source'):
                    article.source = source.contents[1].string.encode("iso-8859-1", "ignore").decode("utf-8", "ignore")
                    break
                for date in xarticle.findAll('date'):
                    article.date = date.contents[0].string
                for body in xarticle.findAll('body'):
                    article.body = body.contents[0].string.strip().encode("iso-8859-1", "ignore").decode("utf-8",
                                                                                                         "ignore")
                article_id = get_dailynews(c, article.title, article.team_id)
                if article_id is None:
                    insertdata.append("('',''," + str(article.league_id) + ",'" + conn.escape_string(
                        article.title) + "','" + conn.escape_string(article.source) + "'," + str(
                        article.team_id) + ",'" + article.date + "','" + conn.escape_string(article.body) + "')")
            #                insert_dailynews(c,article)

            page.close()

    screen = 'breaking-news'

    d = feedparser.parse(
        "http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + newstime + "T12:42:13")

    items = []

    if len(d['entries']):
        for item in d.entries:
            if (item.link.find('/' + direct + '/') > 0):
                if (item.link.find('/' + str(news) + '/') > 0 and news != False):
                    items.append(str(item.link))
                else:
                    items.append(str(item.link))

        for item in items:
            page = urllib2.urlopen(item)
            soup = BeautifulStoneSoup(page)
            for xarticle in soup.findAll('article'):
                article = Article()
                tid = get_league(c, league)
                article.league_id = tid[0]
                for title in xarticle.findAll('title'):
                    article.title = title.contents[0].string.encode("iso-8859-1", "ignore").decode("utf-8", "ignore")
                for source in xarticle.findAll('source'):
                    article.source = source.contents[1].string.encode("iso-8859-1", "ignore").decode("utf-8", "ignore")
                    break
                for author in xarticle.findAll('author'):
                    article.author = author.contents[0].string.encode("iso-8859-1", "ignore").decode("utf-8", "ignore")
                for date in xarticle.findAll('date'):
                    article.date = date.contents[0].string
                for body in xarticle.findAll('body'):
                    article.body = body.contents[0].string.strip().encode("iso-8859-1", "ignore").decode("utf-8",
                                                                                                         "ignore")
                article_id = get_breakingnews(c, article.title, article.league_id)
                if article_id is None:
                    insertdata.append("('',''," + str(article.league_id) + ",'" + conn.escape_string(
                        article.title) + "','" + conn.escape_string(article.source) + "'," + str(
                        article.team_id) + ",'" + article.date + "','" + conn.escape_string(article.body) + "')")

            page.close()
    data = str.join(',', insertdata)
    insert_dailynews(c, data)

    conn.commit()
    c.close()
    conn.close()
except MySQLdb.Error, e:
    print "Guru Meditation #%d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
