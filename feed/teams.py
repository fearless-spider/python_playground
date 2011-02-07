import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
import time
from datetime import date, timedelta
import urllib2

screen = 'teams'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
season = sys.argv[4]
news = False


class Team:
    id = 0
    feed_id = ''
    division_feed_id = ''
    conference_feed_id = ''
    season_feed_id = ''
    name = ''
    first = ''
    short = ''
    nick = ''
    city = ''
    state = ''
    country = ''
    totalsalary = ''
    averagesalary = ''
    division_id = 0
    conference_id = 0


class Meta:
    group_id = 0
    meta_key = ''
    meta_value = ''


class Season:
    id = 0
    feed_id = ''
    name = ''
    stardate = ''
    enddate = ''
    league_id = 0


class Conference:
    id = 0
    feed_id = ''
    name = ''
    short = ''
    season_id = 0


class Division:
    id = 0
    feed_id = ''
    name = ''
    short = ''
    active = 1
    conference_id = 0


conn = MySQLdb.connect("localhost", "", "", "")

c = conn.cursor()


def get_group(c, league):
    c.execute("SELECT id FROM wp_bp_groups WHERE name = '%s'" % league)
    return c.fetchone()


def get_league(c, league):
    c.execute("SELECT id FROM wp_bp_leagues WHERE short = '%s'" % league)
    return c.fetchone()


def get_season(c, feedid):
    c.execute("SELECT id FROM wp_bp_seasons WHERE feed_id = '%s'" % feedid)
    return c.fetchone()


def get_conference(c, feedid):
    c.execute("SELECT id FROM wp_bp_conferences WHERE feed_id = '%s'" % feedid)
    return c.fetchone()


def get_division(c, feedid):
    c.execute("SELECT id FROM wp_bp_divisions WHERE feed_id = '%s'" % feedid)
    return c.fetchone()


def get_team(c, feedid):
    c.execute("SELECT id FROM wp_bp_teams WHERE feed_id = '%s'" % feedid)
    return c.fetchone()


def insert_season(c, data):
    sql = "INSERT INTO wp_bp_seasons(feed_id,name,startdate,enddate,league_id) VALUES ('%s','%s','%s','%s',%d);" % (
    data.feed_id, conn.escape_string(data.name), data.startdate, data.enddate, data.league_id)
    print sql
    c.execute(sql)


def insert_conference(c, data):
    sql = "INSERT INTO wp_bp_conferences(feed_id,name,short,season_id) VALUES ('%s','%s','%s',%d);" % (
    data.feed_id, conn.escape_string(data.name), data.short, data.season_id)
    print sql
    c.execute(sql)


def insert_division(c, data):
    sql = "INSERT INTO wp_bp_divisions(feed_id,name,short,active,conference_id) VALUES ('%s','%s','%s',%d,%d);" % (
    data.feed_id, conn.escape_string(data.name), data.short, data.active, data.conference_id)
    print sql
    c.execute(sql)


def insert_team(c, data):
    sql = "INSERT INTO wp_bp_teams(feed_id,division_feed_id,conference_feed_id,season_feed_id,name,first,nick,short,city,state,country,totalsalary,averagesalary,division_id,conference_id) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%d);" % (
    data.feed_id, data.division_feed_id, data.conference_feed_id, data.season_feed_id, conn.escape_string(data.name),
    conn.escape_string(data.first), conn.escape_string(data.nick), data.short, conn.escape_string(data.city),
    data.state, data.country, data.totalsalary, data.averagesalary, data.division_id, data.conference_id)
    print sql
    c.execute(sql)


def insert_group(c, data):
    sql = """INSERT INTO wp_bp_groups(
                    `creator_id`,
                    `name`,
                    `slug`,
                    `description`,
                    `status`,
                    `enable_forum`,
                    `date_created`,
                    `parent_id`,
                    `xmlurl`,
                    `type`
                ) VALUES (
                    %d, '%s', '%s', '%s', '%s', %d, '%s', %d, '%s', '%s'
                );""" % (
        1,
        data.first + ' ' + data.nick,
        str(data.short) + '-' + str(time.time()),
        '',
        'public',
        0,
        date.today().isoformat(),
        data.parent_id,
        data.feed_id,
        'team'
    )
    print sql
    c.execute(sql)


def insert_groupmeta(c, data):
    sql = "INSERT INTO wp_bp_groups_groupmeta(group_id,meta_key,meta_value) VALUES (%d,'%s','%s');" % (
    data.group_id, data.meta_key, data.meta_value)
    print sql
    c.execute(sql)


d = feedparser.parse("http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "/" + season)

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
                insert_season(c, season)
                season_id = conn.insert_id()
            else:
                season_id = sid[0]
        for xconferencecontent in soup.findAll('conference-content'):
            for xconference in xconferencecontent.findAll('conference'):
                conference = Conference()
                conference.feed_id = xconference.contents[0].string
                conference.name = xconference.contents[1].string
                conference.short = xconference.contents[2].string
                conference.season_id = season_id
                cid = get_conference(c, conference.feed_id)
                if cid is None:
                    insert_conference(c, conference)
                    conference_id = conn.insert_id()
                else:
                    conference_id = cid[0]
            if len(xconferencecontent.findAll('division-content')):
                for xdivisioncontent in xconferencecontent.findAll('division-content'):
                    for xdivision in xdivisioncontent.findAll('division'):
                        division = Division()
                        division.feed_id = xdivision.contents[0].string
                        division.name = xdivision.contents[1].string
                        active = xdivision.contents[2].string
                        if active == 'False':
                            division.active = 0
                        else:
                            division.active = 1
                        division.conference_id = conference_id
                        did = get_division(c, division.feed_id)
                        if did is None:
                            insert_division(c, division)
                            division_id = conn.insert_id()
                        else:
                            division_id = did[0]
                    for xteam in xdivisioncontent.findAll('team'):
                        team = Team()
                        team.conference_feed_id = conference.feed_id
                        team.division_feed_id = division.feed_id
                        team.season_feed_id = season.feed_id
                        team.feed_id = xteam.contents[0].string
                        names = {}
                        for tname in xteam.findAll('name'):
                            names[tname.get('type')] = tname.string
                        team.name = names.get('name')
                        team.first = names.get('first')
                        team.nick = names.get('nick')
                        team.short = names.get('short')
                        for city in xteam.findAll('city'):
                            team.city = city.contents[0].string
                        for state in xteam.findAll('state'):
                            team.state = state.contents[0].string
                        for country in xteam.findAll('country'):
                            team.country = country.contents[0].string
                        for totalsalary in xteam.findAll('total-salary'):
                            team.totalsalary = totalsalary.contents[0].string
                        for averagesalary in xteam.findAll('average-salary'):
                            team.averagesalary = averagesalary.contents[0].string
                        team.division_id = division_id
                        team.conference_id = conference_id
                        tid = get_team(c, team.feed_id)
                        if tid is None:
                            insert_team(c, team)
                            parent_id = get_group(c, league)
                            team.parent_id = parent_id[0]
                            insert_group(c, team)
                            group_id = conn.insert_id()
                            meta = Meta()
                            meta.group_id = group_id
                            meta.meta_key = 'last_activity'
                            meta.meta_value = '2011-01-14 23:32:44'
                            insert_groupmeta(c, meta)
                            meta = Meta()
                            meta.group_id = group_id
                            meta.meta_key = 'total_member_count'
                            meta.meta_value = '1'
                            insert_groupmeta(c, meta)
                            meta = Meta()
                            meta.group_id = group_id
                            meta.meta_key = 'bp_group_hierarchy_subgroup_creators'
                            meta.meta_value = 'groups_admins'
                            insert_groupmeta(c, meta)
            else:
                for xteam in xconferencecontent.findAll('team'):
                    team = Team()
                    team.conference_feed_id = conference.feed_id
                    team.division_feed_id = ''
                    team.season_feed_id = season.feed_id
                    team.feed_id = xteam.contents[0].string
                    team.name = xteam.contents[1].string
                    team.first = xteam.contents[2].string
                    team.nick = xteam.contents[3].string
                    team.short = xteam.contents[4].string
                    for city in xteam.findAll('city'):
                        team.city = city.contents[0].string
                    for state in xteam.findAll('state'):
                        team.state = state.contents[0].string
                    for country in xteam.findAll('country'):
                        team.country = country.contents[0].string
                    for totalsalary in xteam.findAll('total-salary'):
                        team.totalsalary = totalsalary.contents[0].string
                    for averagesalary in xteam.findAll('average-salary'):
                        team.averagesalary = averagesalary.contents[0].string
                    team.division_id = 0
                    team.conference_id = conference_id
                    tid = get_team(c, team.feed_id)
                    if tid is None:
                        insert_team(c, team)
                        parent_id = get_group(c, league)
                        team.parent_id = parent_id[0]
                        insert_group(c, team)
                        group_id = conn.insert_id()
                        meta = Meta()
                        meta.group_id = group_id
                        meta.meta_key = 'last_activity'
                        meta.meta_value = '2011-01-14 23:32:44'
                        insert_groupmeta(c, meta)
                        meta = Meta()
                        meta.group_id = group_id
                        meta.meta_key = 'total_member_count'
                        meta.meta_value = '1'
                        insert_groupmeta(c, meta)
                        meta = Meta()
                        meta.group_id = group_id
                        meta.meta_key = 'bp_group_hierarchy_subgroup_creators'
                        meta.meta_value = 'groups_admins'
                        insert_groupmeta(c, meta)
        page.close()

conn.commit()
