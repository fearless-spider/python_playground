import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
from datetime import date, timedelta, datetime
import time
import urllib2

#####
timedifference = datetime.today() - timedelta(days=15)
#####

screen = 'schedules'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
news = False


class Meta:
    event_id = 0
    meta_key = ''
    meta_value = ''


class Venue:
    id = 0
    feed_id = ''
    name = ''
    short = ''
    city = ''
    state = ''
    country = ''
    capacity = ''
    fieldtype = ''


class Competition:
    id = 0
    feed_id = ''
    name = ''
    startdate = ''
    status = ''
    gametype = ''
    neutralsite = ''
    daygame = 0
    datetbd = ''
    home_id = 0
    away_id = 0
    season_id = 0
    venue_id = 0


class Event:
    id = ''
    name = ''
    type = ''
    description = ''
    country = ''
    state = ''
    city = ''
    address = ''
    note = ''
    startdate = ''
    enddate = ''
    starthour = ''
    endhour = ''
    startmin = ''
    endmin = ''
    startunix = ''
    endunix = ''
    grouplink = ''
    grouplinkvs = ''


conn = MySQLdb.connect("localhost", "", "", "")

c = conn.cursor()


def get_season(c, feedid):
    c.execute("SELECT id FROM wp_bp_seasons WHERE feed_id = '%s'" % feedid)
    return c.fetchone()


def get_team_by_feedid(c, feedid):
    c.execute("SELECT id,CONCAT_WS(' ',first,nick) AS name FROM wp_bp_teams WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_group_by_feedid(c, feedid):
    c.execute("SELECT id FROM wp_bp_groups WHERE xmlurl = '%s'" % (feedid))
    return c.fetchone()


def get_venue(c, feedid):
    c.execute("SELECT id FROM wp_bp_venues WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_competition(c, feedid):
    c.execute("SELECT id FROM wp_bp_competitions WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def insert_venue(c, data):
    sql = """INSERT INTO wp_bp_venues(
                    `feed_id`,
                    `name`,
                    `short`,
                    `city`,
                    `state`,
                    `country`,
                    `capacity`,
                    `fieldtype`
    ) VALUES (
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s'
    );""" % (
        data.feed_id,
        data.name,
        data.short,
        data.city,
        data.state,
        data.country,
        data.capacity,
        data.fieldtype
    )
    print sql
    c.execute(sql)


def insert_competition(c, data):
    sql = """INSERT INTO wp_bp_competitions(
                    `feed_id`,
                    `name`,
                    `startdate`,
                    `status`,
                    `gametype`,
                    `neutralsite`,
                    `daygame`,
                    `datetbd`,
                    `home_id`,
                    `away_id`,
                    `season_id`,
                    `venue_id`
    ) VALUES (
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    %d,
                    '%s',
                    %d,
                    %d,
                    %d,
                    %d
    );""" % (
        data.feed_id,
        data.name,
        data.startdate,
        data.status,
        data.gametype,
        data.neutralsite,
        data.daygame,
        data.datetbd,
        data.home_id,
        data.away_id,
        data.season_id,
        data.venue_id
    )
    print sql
    c.execute(sql)


def insert_event(c, data):
    sql = """INSERT INTO wp_jet_events(
                    `creator_id`,
                    `name`,
                    `etype`,
                    `eventapproved`,
                    `slug`,
                    `description`,
                    `eventterms`,
                    `placedcountry`,
                    `placedstate`,
                    `placedcity`,
                    `placedaddress`,
                    `placednote`,
                    `placedgooglemap`,
                    `flyer`,
                    `newspublic`,
                    `newsprivate`,
                    `edtsd`,
                    `edted`,
                    `edtsth`,
                    `edteth`,
                    `edtstm`,
                    `edtetm`,
                    `edtsdunix`,
                    `edtedunix`,
                    `status`,
                    `grouplink`,
                    `grouplinkvs`,
                    `forumlink`,
                    `enablesocial`,
                    `enable_forum`,
                    `date_created`,
                    `notify_timed_enable`
    ) VALUES (
                    %d,
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    %d,
                    %d,
                    '%s',
                    '%s'
    );""" % (
        1,
        data.name,
        data.type,
        1,
        data.name.strip().replace(' ', '') + '-' + str(time.time()),
        data.description,
        '',
        data.country,
        data.state,
        data.city,
        data.address,
        data.note,
        '',
        '',
        '',
        '',
        data.startdate,
        data.enddate,
        data.starthour,
        data.endhour,
        data.startmin,
        data.endmin,
        data.startunix,
        data.endunix,
        'public',
        data.grouplink,
        data.grouplinkvs,
        1,
        1,
        0,
        '2011-01-07',
        ''
    )
    print sql
    c.execute(sql)


def insert_eventmeta(c, data):
    sql = "INSERT INTO wp_jet_events_eventmeta(event_id,meta_key,meta_value) VALUES (%d,'%s','%s');" % (
    data.event_id, data.meta_key, data.meta_value)
    print sql
    c.execute(sql)


d = feedparser.parse(
    "http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + timedifference.strftime(
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
            sid = get_season(c, xseason.contents[0].string)
            if sid is not None:
                season_id = int(sid[0])
        for xcompetition in soup.findAll('competition'):
            event = Event()
            competition = Competition()
            for xid in xcompetition.findAll('id'):
                competition.feed_id = xid.string
                break
            for xname in xcompetition.findAll('name'):
                competition.name = xname.string
                break
            for xstartdate in xcompetition.findAll('start-date'):
                competition.startdate = xstartdate.string
            for xstatus in xcompetition.findAll('competition-status'):
                competition.status = xstatus.string
            for xgametype in xcompetition.findAll('competition-type'):
                competition.gametype = xgametype.string
            for xneutralsite in xcompetition.findAll('neutral-site'):
                competition.neutralsite = xneutralsite.string
            for xdaygame in xcompetition.findAll('day'):
                if xdaygame.string:
                    day = 1
                else:
                    day = 0
                competition.daygame = day
            for xdatetbd in xcompetition.findAll('date-tbd'):
                competition.datetbd = xdatetbd.string
            for xhometeamcontent in xcompetition.findAll('home-team-content'):
                feedid = xhometeamcontent.contents[0].contents[0].string
                hid = get_team_by_feedid(c, feedid)
                ghid = get_group_by_feedid(c, feedid)
                if hid is not None:
                    competition.home_id = int(hid[0])
                    ghome_id = int(ghid[0])
            for xawayteamcontent in xcompetition.findAll('away-team-content'):
                feedid = xawayteamcontent.contents[0].contents[0].string
                aid = get_team_by_feedid(c, feedid)
                gaid = get_group_by_feedid(c, feedid)
                if aid is not None:
                    competition.away_id = int(aid[0])
                    gaway_id = int(gaid[0])
            competition.season_id = season_id
            for xvenue in xcompetition.findAll('venue'):
                venue = Venue()
                venue.feed_id = xvenue.contents[0].string
                venue.name = xvenue.contents[1].string
                venue.short = xvenue.contents[2].string
                for xcity in xvenue.findAll('city'):
                    venue.city = xcity.string
                for xstate in xvenue.findAll('state'):
                    venue.state = xstate.string
                for xcountry in xvenue.findAll('country'):
                    venue.country = xcountry.string
                for xcapacity in xvenue.findAll('capacity'):
                    venue.capacity = xcapacity.string
                for xfieldtype in xvenue.findAll('fieldtype'):
                    venue.fieldtype = xfieldtype.string
                vid = get_venue(c, venue.feed_id)
                if vid is None:
                    insert_venue(c, venue)
                    competition.venue_id = conn.insert_id()
                else:
                    competition.venue_id = int(vid[0])
                cid = get_competition(c, competition.feed_id)
                if cid is None:
                    insert_competition(c, competition)

                    event.name = str(hid[1]) + ' VS ' + str(aid[1])
                    event.type = competition.gametype
                    event.description = event.name
                    event.country = venue.country
                    event.city = venue.city
                    event.state = venue.state
                    event.address = venue.name
                    event.note = venue.capacity
                    date = competition.startdate[0:competition.startdate.find('T')] + ' ' + competition.startdate[
                                                                                            competition.startdate.find(
                                                                                                'T') + 1:19]
                    d = time.strptime(date, "%Y-%m-%d %H:%M:%S")
                    event.startdate = datetime.fromtimestamp(time.mktime(d)).strftime("%d/%m/%Y")
                    event.enddate = datetime.fromtimestamp(time.mktime(d)).strftime("%d/%m/%Y")
                    event.starthour = competition.startdate[competition.startdate.find('T') + 1:13]
                    event.endhour = competition.startdate[competition.startdate.find('T') + 1:13]
                    event.startmin = competition.startdate[competition.startdate.find('T') + 4:16]
                    event.endmin = competition.startdate[competition.startdate.find('T') + 4:16]
                    d = time.strptime(date, "%Y-%m-%d %H:%M:%S")
                    event.startunix = str(time.mktime(d))[0:10]
                    event.endunix = str(time.mktime(d))[0:10]
                    event.grouplink = ghome_id
                    event.grouplinkvs = gaway_id
                    insert_event(c, event)
                    event_id = conn.insert_id()
                    meta = Meta()
                    meta.event_id = event_id
                    meta.meta_key = 'last_activity'
                    meta.meta_value = '2011-01-14 23:32:44'
                    insert_eventmeta(c, meta)
                    meta = Meta()
                    meta.event_id = event_id
                    meta.meta_key = 'total_member_count'
                    meta.meta_value = '1'
                    insert_eventmeta(c, meta)
        page.close()
conn.commit()
