# -*- coding: utf-8 -*-

from datetime import date
import re

from statsutils import Member, Meta, replace_nonascii, slugfy, debug

if debug:
    import pymysql as MySQLdb
else:
    import MySQLdb

__author__ = 'fearless'


def db_open():
    conn = None
    if debug:
        conn = MySQLdb.connect(host="localhost", port=8889, user="", passwd="", db="")
    else:
        conn = MySQLdb.connect("", "", "", "")
    c = conn.cursor()
    return (c, conn)


def db_close(c, conn):
    conn.commit()
    c.close()
    conn.close()


def get_score(c, competition_id):
    c.execute("SELECT id FROM wp_bp_teams_boxscores WHERE competition_id = '%s'" % (competition_id))
    return c.fetchone()


def get_records(c, competition_id, team_id):
    c.execute("SELECT id FROM wp_bp_boxscores_records WHERE competition_id = '%s' AND team_global_id = '%s'" % (
        competition_id, team_id))
    return c.fetchone()


def get_stats(c, global_id, season):
    c.execute(
        "SELECT `id`, `group`, `type`, `split` FROM `wp_bp_teams_players_stats` WHERE `player_global_id` = %s AND `season` = %s" % (
            int(global_id), season))
    return c.fetchall()


def get_players(c, season):
    c.execute("SELECT id, global_id FROM wp_bp_teams_players WHERE season = '%s';" % (season))
    return c.fetchall()


def get_teams_with_players(c):
    c.execute(
        "SELECT t.global_id AS team_global_id, p.global_id AS player_global_id FROM wp_bp_teams_players p INNER JOIN wp_bp_teams t ON t.id = p.team_id;")
    return c.fetchall()


def get_stands(c, team_id, season):
    c.execute(
        "SELECT `id`, `group`, `type`, `name` FROM `wp_bp_teams_standings` WHERE `team_id` = %d AND `season` = '%s';" % (
            team_id, season))
    return c.fetchall()


def insert_standings(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_teams_standings (
                    `id`,
                    `group`,
                    `type`,
                    `name`,
                    `num`,
                    `num2`,
                    `num3`,
                    `num4`,
                    `team_id`,
                    `season`,
                    `global_id`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `num` = VALUES(`num`),
        `num2` = VALUES(`num2`),
        `num3` = VALUES(`num3`),
        `num4` = VALUES(`num4`),
        `global_id` = VALUES(`global_id`)
        ;""" % data
        c.execute(sql)


def get_all_teams(c):
    c.execute(
        "SELECT g.id,t.name,t.city,t.alias,g.slug,g.parent_id,g.name FROM wp_bp_groups g LEFT JOIN wp_bp_teams t ON t.group_id = g.id WHERE g.`type`='team' ORDER BY t.league;")
    # c.execute("SELECT id, global_id FROM wp_bp_teams;")
    return c.fetchall()


def get_parent(c, parent):
    c.execute("SELECT g.slug FROM wp_bp_groups g WHERE g.id=%d;" % parent)
    return c.fetchone()


def get_teams(c, league_name):
    c.execute("SELECT id, global_id FROM wp_bp_teams WHERE league = '%s';" % (league_name))
    # c.execute("SELECT id, global_id FROM wp_bp_teams;")
    return c.fetchall()


def get_finalstats(c, competition_id):
    c.execute("SELECT `id` FROM `wp_bp_boxscores_competition` WHERE `gamecode` = '%s';" % (competition_id))
    return c.fetchone()


# start stories
def get_stories(c, code):
    c.execute("SELECT `id`, `story_id` FROM `wp_bp_stories` WHERE `code` = '%s';" % (code))
    return c.fetchall()


def insert_stories(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_stories (
                    `id`,
                    `published_at`,
                    `story_id`,
                    `code`,
                    `slug`,
                    `version`,
                    `headline`,
                    `content`,
                    `byline`,
                    `bytitle`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `published_at` = VALUES(`published_at`),
        `headline` = VALUES(`headline`),
        `content` = VALUES(`content`),
        `version` = VALUES(`version`),
        `byline` = VALUES(`byline`),
        `bytitle` = VALUES(`bytitle`)
        ;""" % data
        c.execute(sql)


def insert_images(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_story_images (
                    `id`,
                    `story_id`,
                    `source`,
                    `caption`,
                    `image_id`
        ) VALUES %s
        ;""" % data
        c.execute(sql)


def insert_teams_story(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_story_teams (
                    `story_id`,
                    `team_global_id`
        ) VALUES %s
        ;""" % data
        c.execute(sql)


# end stories

# start schedule

def get_event(c, global_id):
    c.execute("SELECT id FROM wp_jet_events WHERE global_id = '%s'" % (global_id))
    return c.fetchone()


def get_eventmeta(c, data):
    c.execute("SELECT id FROM wp_jet_events_eventmeta WHERE event_id = %d AND meta_key = '%s'" % (
        data.event_id, data.meta_key))
    return c.fetchone()


def del_eventmeta(c, event_id):
    c.execute("DELETE FROM wp_jet_events_eventmeta WHERE event_id = %d" % (event_id))


def get_members(c, data):
    c.execute("SELECT id FROM wp_jet_events_members WHERE event_id = %d" % (data.group_id))
    return c.fetchall()


def insert_eventmeta(c, data):
    sql = "INSERT INTO wp_jet_events_eventmeta(event_id,meta_key,meta_value) VALUES (%d,'%s','%s');" % (
        data.event_id, data.meta_key, data.meta_value)
    c.execute(sql)


def insert_group_member(c, data):
    sql = "INSERT INTO wp_jet_events_members(event_id,user_id,inviter_id,is_admin,date_modified,is_confirmed,user_title) VALUES (%d,'%d','%d','%d','%s','%d','%s');" % (
        data.group_id, data.user_id, data.inviter_id, data.is_admin, date.today().isoformat(), data.is_confirmed,
        data.user_title)
    # print sql
    c.execute(sql)


def insert_events(c, conn, data, event_id):
    if data != '':
        sql = """INSERT INTO wp_jet_events(
            `id`,
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
            `notify_timed_enable`,
            `season`,
            `global_id`,
            `league`
            ) VALUES %s
            ON DUPLICATE KEY UPDATE
            `grouplink` = VALUES(`grouplink`),
            `grouplinkvs` = VALUES(`grouplinkvs`),
            `name` = VALUES(`name`),
            `slug` = VALUES(`slug`),
            `description` = VALUES(`description`),
            `placedcountry` = VALUES(`placedcountry`),
            `placedstate` = VALUES(`placedstate`),
            `placedcity` = VALUES(`placedcity`),
            `placedaddress` = VALUES(`placedaddress`),
            `placednote` = VALUES(`placednote`),
            `edtsd` = VALUES(`edtsd`),
            `edted` = VALUES(`edted`),
            `edtsth` = VALUES(`edtsth`),
            `edteth` = VALUES(`edteth`),
            `edtstm` = VALUES(`edtstm`),
            `edtetm` = VALUES(`edtetm`),
            `edtsdunix` = VALUES(`edtsdunix`),
            `edtedunix` = VALUES(`edtedunix`),
            `status` = VALUES(`status`),
            `league` = VALUES(`league`)
            ;""" % data
        c.execute(sql)
        if not event_id:
            event_id = conn.insert_id()
        del_eventmeta(c, event_id)
        meta = Meta()
        meta.event_id = event_id
        meta.meta_key = 'last_activity'
        meta.meta_value = '2011-06-14 23:32:44'
        if get_eventmeta(c, meta) is None:
            insert_eventmeta(c, meta)
        meta = Meta()
        meta.event_id = event_id
        meta.meta_key = 'total_member_count'
        meta.meta_value = '1'
        if get_eventmeta(c, meta) is None:
            insert_eventmeta(c, meta)
        member = Member()
        member.group_id = event_id
        if get_members(c, member) is None:
            insert_group_member(c, member)


def get_teams_group(c, league_name):
    c.execute("SELECT group_id, global_id FROM wp_bp_teams WHERE league = '%s';" % (league_name))
    return c.fetchall()


# end schedule

# start player stats
def insert_stats(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_teams_players_stats (
                    `id`,
                    `group`,
                    `type`,
                    `num`,
                    `player_global_id`,
                    `season`,
                    `split`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `num` = VALUES(`num`)
        ;""" % data
        c.execute(sql)


# end player stats

# start live
def get_score(c, competition_id):
    c.execute("SELECT id FROM wp_bp_teams_boxscores WHERE competition_id = '%s'" % (competition_id))
    return c.fetchone()


# end live

# start finalstats
def insert_boxscores(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_teams_boxscores(
            `id`,
            `league_id`,
            `start_date`,
            `status`,
            `home_team_short`,
            `home_team_id`,
            `home_score`,
            `away_team_short`,
            `away_team_id`,
            `away_score`,
            `competition_id`,
            `period`,
            `period_time`
            ) VALUES %s
            ON DUPLICATE KEY UPDATE
            `league_id` = VALUES(`league_id`),
            `status` = VALUES(`status`),
            `start_date` = VALUES(`start_date`),
            `home_score` = VALUES(`home_score`),
            `away_score` = VALUES(`away_score`),
            `period` = VALUES(`period`),
            `period_time` = VALUES(`period_time`)
            ;""" % data
        c.execute(sql)


def insert_teamstats(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_boxscores_teamstats (
                    `id`,
                    `stat_type`,
                    `stat`,
                    `value`,
                    `competition_id`,
                    `team_global_id`,
                    `home`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `value` = VALUES(`value`)
        ;""" % data
        c.execute(sql)


def insert_playerstats(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_boxscores_playerstats (
                    `id`,
                    `stat_type`,
                    `stat`,
                    `value`,
                    `competition_id`,
                    `player_global_id`,
                    `team_global_id`,
                    `split`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `value` = VALUES(`value`)
        ;""" % data
        c.execute(sql)


def insert_linescores(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_boxscores_linescores (
                    `id`,
                    `quarter`,
                    `score`,
                    `num1`,
                    `num2`,
                    `competition_id`,
                    `team_global_id`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `score` = VALUES(`score`),
        `num1` = VALUES(`num1`),
        `num2` = VALUES(`num2`)
        ;""" % data
        c.execute(sql)


def insert_records(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_boxscores_records (
                    `competition_id`,
                    `wins`,
                    `losses`,
                    `pct`,
                    `team_global_id`
        ) VALUES %s
        ;""" % data
        c.execute(sql)


def insert_scores(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_boxscores_scores (
                    `id`,
                    `competition_id`,
                    `type_id`,
                    `num`,
                    `team_global_id`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `num` = VALUES(`num`)
        ;""" % data
        c.execute(sql)


def insert_competitions(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_boxscores_competition (
                    `id`,
                    `gamecode`,
                    `gametype`,
                    `stadium_name`,
                    `stadium_city`,
                    `stadium_state`,
                    `stadium_country`,
                    `date`,
                    `gamestate`,
                    `away_team_name`,
                    `away_team_city`,
                    `away_team_alias`,
                    `away_team_global_id`,
                    `away_team_score`,
                    `home_team_name`,
                    `home_team_city`,
                    `home_team_alias`,
                    `home_team_global_id`,
                    `home_team_score`,
                    `season`,
                    `league`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `gamestate` = VALUES(`gamestate`),
        `away_team_score` = VALUES(`away_team_score`),
        `home_team_score` = VALUES(`home_team_score`)
        ;""" % data
        c.execute(sql)


# end finalstats

# start roster
def insert_players(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_teams_players (
                    `id`,
                    `firstname`,
                    `lastname`,
                    `team_id`,
                    `height`,
                    `weight`,
                    `birthdate`,
                    `birthcity`,
                    `birthstate`,
                    `birthcountry`,
                    `number`,
                    `position`,
                    `status`,
                    `global_id`,
                    `school`,
                    `highschool_name`,
                    `highschool_city`,
                    `first_year`,
                    `rookie_year`,
                    `experience`,
                    `suspended`,
                    `season`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `team_id` = VALUES(`team_id`),
        `firstname` = VALUES(`firstname`),
        `lastname` = VALUES(`lastname`),
        `height` = VALUES(`height`),
        `weight` = VALUES(`weight`),
        `number` = VALUES(`number`),
        `position` = VALUES(`position`),
        `birthstate` = VALUES(`birthstate`),
        `birthcountry` = VALUES(`birthcountry`),
        `status` = VALUES(`status`),
        `experience` = VALUES(`experience`),
        `suspended` = VALUES(`suspended`)
        ;""" % data

        c.execute(sql)
        # return sql
        # end roster


def get_groups(c, parent_id):
    c.execute("SELECT id, global_id FROM wp_bp_groups WHERE parent_id = %d;" % (parent_id))
    return c.fetchall()


def insert_groupmeta(c, data):
    sql = "INSERT INTO wp_bp_groups_groupmeta(group_id,meta_key,meta_value) VALUES (%d,'%s','%s');" % (
        data.group_id, data.meta_key, data.meta_value)
    # print sql
    c.execute(sql)


def insert_group_member(c, data):
    sql = "INSERT INTO wp_bp_groups_members(group_id,user_id,inviter_id,is_admin,date_modified,is_confirmed,user_title) VALUES (%d,'%d','%d','%d','%s','%d','%s');" % (
        data.group_id, data.user_id, data.inviter_id, data.is_admin, date.today().isoformat(), data.is_confirmed,
        data.user_title)
    # print sql
    c.execute(sql)


def insert_group(c, conn, data):
    if data != '':
        sql = """INSERT INTO wp_bp_groups (
                    `creator_id`,
                    `name`,
                    `slug`,
                    `description`,
                    `status`,
                    `enable_forum`,
                    `date_created`,
                    `parent_id`,
                    `type`,
                    `sport`,
                    `pro`,
                    `city`,
                    `alias`,
                    `state`,
                    `country`,
                    `global_id`
        ) VALUES (
            %d,
            '%s',
            '%s',
            '%s',
            '%s',
            %d,
            '%s',
            %d,
            '%s',
            %d,
            %d,
            '%s',
            '%s',
            '%s',
            '%s',
            '%s'
            )
        ;""" % (
            1,
            replace_nonascii(data.city) + ' ' + replace_nonascii(data.name),
            slugfy(replace_nonascii(data.city) + ' ' + replace_nonascii(data.name) + ' ' + replace_nonascii(
                data.league_name)
                   , "-"),
            '',
            'public',
            0,
            date.today().isoformat(),
            data.parent_id,
            'team',
            data.sport,
            1,
            replace_nonascii(data.city),
            re.escape(data.alias),
            replace_nonascii(data.state),
            replace_nonascii(data.country),
            data.global_id
        )
        c.execute(sql)
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
        member = Member()
        member.group_id = group_id
        insert_group_member(c, member)

        return group_id


def insert_teams(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_teams (
                    `id`,
                    `group_id`,
                    `global_id`,
                    `city`,
                    `name`,
                    `alias`,
                    `season`,
                    `conference`,
                    `division`,
                    `league`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `alias` = VALUES(`alias`),
        `city` = VALUES(`city`),
        `name` = VALUES(`name`),
        `season` = VALUES(`season`),
        `conference` = VALUES(`conference`),
        `division` = VALUES(`division`),
        `league` = VALUES(`league`)
        ;""" % data
        c.execute(sql)


# leaders

def get_leaders(c, season, league_name, category, conference):
    c.execute(
        "SELECT id, global_id FROM wp_bp_teams_leaders WHERE season = '%s' AND league = '%s' AND category = '%s' AND conference = '%s';" % (
            season, league_name, category, conference))
    return c.fetchall()


def insert_leaders(c, data):
    if data != '':
        sql = """INSERT INTO wp_bp_teams_leaders (
                    `id`,
                    `global_id`,
                    `category`,
                    `category_heading`,
                    `firstname`,
                    `lastname`,
                    `alias`,
                    `ranking`,
                    `stat`,
                    `tie`,
                    `season`,
                    `league`,
                    `conference`
        ) VALUES %s
        ON DUPLICATE KEY UPDATE
        `ranking` = VALUES(`ranking`),
        `stat` = VALUES(`stat`),
        `tie` = VALUES(`tie`),
        `alias` = VALUES(`alias`),
        `conference` = VALUES(`conference`)
        ;""" % data
        c.execute(sql)


def get_twitters(c, item_id):
    c.execute(
        "SELECT component, type, action, content, primary_link, date_recorded, item_id, tweet_id, profile_picture FROM wp_bp_twitter WHERE item_id = '%s' order by date_recorded desc" % (
            item_id)
    )
    return c.fetchall()


def activity_exists(c, tweet):
    c.execute("SELECT COUNT(id) FROM wp_bp_activity WHERE tweet_id = '%s'" % tweet)
    return c.fetchone()


def insert_activity(c, data):
    if (data != ''):
        sql = "INSERT INTO wp_bp_activity( user_id, component, type, action, content, primary_link, date_recorded, item_id, tweet_id, profile_picture ) VALUES %s " % data
        c.execute(sql)


def tweet_exists(c, tweet):
    c.execute("SELECT COUNT(id) FROM wp_bp_activity WHERE tweet_id = '%s'" % tweet['id_str'])
    return c.fetchone()


def insert_twitt(c, data):
    if (data != ''):
        sql = "INSERT INTO wp_bp_twitter( user_id, component, type, action, content, primary_link, date_recorded, item_id, tweet_id, profile_picture ) VALUES %s " % data
        c.execute(sql)


def get_twitter_teams(c):
    sql = "SELECT twitter_id, group_id FROM wp_bp_twitter_teams WHERE twitter_id IS NOT NULL"
    c.execute(sql)
    return c.fetchall()


def get_twitter_teams_null(c):
    sql = "SELECT id,twitter FROM wp_bp_twitter_teams WHERE twitter_id IS NULL"
    c.execute(sql)
    return c.fetchall()


def update_twitter_team(c, twitter_id, id):
    sql = "UPDATE wp_bp_twitter_teams SET twitter_id = '%s' WHERE id = %d" % (twitter_id, id)
    c.execute(sql)
