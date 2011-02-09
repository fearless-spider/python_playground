import sys
import MySQLdb
from BeautifulSoup import BeautifulStoneSoup
import feedparser
from datetime import date, timedelta
import urllib2

screen = 'player-stats'
sport = sys.argv[1]
league = sys.argv[2]
direct = sys.argv[3]
# season = sys.argv[4]
news = False


class PlayerStats:
    id = 0
    player_feed_id = ''
    team_feed_id = ''
    season_feed_id = ''
    league_id = 0
    season_name = ''
    player_id = 0


class StatsBasketball:
    type = ''
    games_played = 0
    games_started = 0
    seconds_played = 0
    points = 0
    points_highest = 0
    field_goals_made = 0
    field_goals_attempted = 0
    three_point_field_goals_made = 0
    three_point_field_goals_attempted = 0
    free_throws_made = 0
    free_throws_attempted = 0
    plus_minus = 0
    assists = 0
    rebounds_offensive = 0
    rebounds_defensive = 0
    steals = 0
    turnovers = 0
    blocks = 0
    fouls_personal = 0
    fouls_technical = 0


class StatsBaseball:
    type = ''
    games_played = 0
    games_started = 0
    at_bats = 0
    runs = 0
    hits = 0
    doubles = 0
    triples = 0
    home_runs = 0
    total_bases = 0
    runs_batted_in = 0
    walks = 0
    intentional_walks = 0
    strikeouts = 0
    hit_by_pitch = 0
    stolen_bases = 0
    caught_stealing = 0
    sacrifice_hits = 0
    sacrifice_flys = 0
    grounded_into_double_plays = 0
    left_on_base = 0
    two_out_rbi = 0
    rlisp_two_out = 0
    slugging_percentage = 0
    on_base_percentage = 0
    batting_average = 0
    on_base_plus_slugging = 0
    fielding_errors = 0
    passed_balls = 0
    catcher_stealers_caught = 0
    catcher_stealers_allowed = 0
    catcher_interferences = 0
    outfield_assists = 0
    pitcher_games_played = 0
    pitcher_games_started = 0
    quality_starts = 0
    wins = 0
    losses = 0
    no_decisions = 0
    holds = 0
    saves = 0
    blown_saves = 0
    complete_games = 0
    shutouts = 0
    outs_pitched = 0
    earned_run_average = 0
    whip = 0
    pitcher_hits = 0
    pitcher_runs = 0
    pitcher_earned_runs = 0
    pitcher_walks = 0
    pitcher_strikeouts = 0
    pitcher_home_runs = 0
    pitcher_stolen_bases = 0
    pitcher_caught_stealing = 0
    pitcher_intentional_walks = 0
    pitcher_hit_by_pitch = 0
    pitcher_sacrifice_hits = 0
    pitcher_sacrifice_flys = 0
    pitches_thrown = 0
    starting_pitches_thrown = 0
    wild_pitches = 0
    strikes_thrown = 0
    ground_ball_outs = 0
    fly_ball_outs = 0
    batters_faced = 0
    pickoffs = 0
    fielding_errors = 0
    inherited_runners = 0
    inherited_runners_scored = 0
    balks = 0


class StatsHockey:
    type = ''
    games_played = 0
    goals = 0
    goals_period_1 = 0
    goals_period_2 = 0
    goals_period_3 = 0
    goals_overtime = 0
    goals_power_play = 0
    goals_short_handed = 0
    game_winning_goals = 0
    assists = 0
    plus_minus = 0
    penalty_minutes = 0
    shots = 0
    faceoffs_won = 0
    faceoffs_lost = 0
    time_on_ice_secs = 0
    time_on_ice_even_strength_secs = 0
    time_on_ice_power_play_secs = 0
    time_on_ice_short_handed_secs = 0
    shifts = 0


class StatsFootball:
    type = ''
    games_played = 0
    games_started = 0
    starter_games_won = 0
    starter_games_lost = 0
    starter_games_tied = 0
    passer_rating = 0
    rushing_plays = 0
    rushing_gross_yards = 0
    rushing_net_yards = 0
    rushing_lost_yards = 0
    rushing_longest_yards = 0
    rushing_touchdowns = 0
    rushing_touchdowns_longest_yards = 0
    rushing_2pt_conversions_succeeded = 0
    passing_plays_attempted = 0
    passing_plays_completed = 0
    passing_gross_yards = 0
    passing_net_yards = 0
    passing_longest_yards = 0
    passing_plays_intercepted = 0
    passing_plays_sacked = 0
    passing_sacked_yards = 0
    passing_touchdowns = 0
    passing_touchdowns_longest_yards = 0
    passing_2pt_conversions_succeeded = 0
    receiving_targeted = 0
    receiving_receptions = 0
    receiving_yards = 0
    receiving_longest_yards = 0
    receiving_touchdowns = 0
    receiving_touchdowns_longest_yards = 0
    receiving_2pt_conversions_succeeded = 0
    fumbles = 0
    fumbles_lost = 0
    fumbles_recovered_lost_by_opposition = 0
    fumbles_recovered_touchdowns = 0
    fumbles_recovered_touchdowns_longest_yards = 0
    interceptions_returned_touchdowns = 0
    interceptions_returned_touchdowns_longest_yards = 0
    punting_plays = 0
    punting_gross_yards = 0
    punting_net_yards = 0
    punting_touchbacks = 0
    punting_singles = 0
    punting_inside_twenty = 0
    punting_longest_yards = 0
    punt_returns = 0
    punt_return_yards = 0
    punt_return_longest_yards = 0
    punt_return_faircatches = 0
    punt_return_touchdowns = 0
    punt_return_touchdowns_longest_yards = 0
    kickoffs = 0
    kickoff_yards = 0
    kickoff_longest_yards = 0
    kickoff_singles = 0
    kickoff_returns = 0
    kickoff_return_yards = 0
    kickoff_return_longest_yards = 0
    kickoff_return_faircatches = 0
    kickoff_return_touchdowns = 0
    kickoff_return_touchdowns_longest_yards = 0
    extra_point_kicks_attempted = 0
    extra_point_kicks_succeeded = 0
    field_goals_attempted = 0
    field_goals_succeeded = 0
    field_goals_succeeded_yards = 0
    field_goals_succeeded_longest_yards = 0
    field_goals_blocked = 0
    kicking_singles = 0
    defense_interceptions = 0
    defense_interception_yards = 0
    defense_tackles = 0
    defense_solo_tackles = 0
    defense_assisted_tackles = 0
    defense_special_teams_tackles = 0
    defense_special_teams_solo_tackles = 0
    defense_special_teams_assisted_tackles = 0
    defense_misc_solo_tackles = 0
    defense_misc_assisted_tackles = 0
    defense_sacks = 0
    defense_sack_yards = 0
    defense_tackles_for_loss = 0
    defense_tackles_for_loss_yards = 0
    defense_forced_fumbles = 0
    defense_fumble_recoveries = 0
    defense_special_teams_fumble_recoveries = 0
    defense_miscellaneous_fumble_recoveries = 0
    defense_pass_defenses = 0
    penalty_yards = 0
    total_touchdowns = 0


class StatsSoccer:
    type = ''
    goals = 0
    goals_half_1 = 0
    goals_half_2 = 0
    goals_penalty = 0
    goals_scored_first = 0
    own_goals = 0
    yellow_cards = 0
    red_cards = 0
    discipline_points = 0


conn = MySQLdb.connect("localhost", "", "", "")

c = conn.cursor()


def get_league(c, league):
    c.execute("SELECT id FROM wp_bp_leagues WHERE short = '%s'" % (league))
    return c.fetchone()


def get_team_by_feedid(c, feedid):
    c.execute("SELECT id FROM wp_bp_teams WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_player(c, feedid):
    c.execute("SELECT id FROM wp_bp_teams_players WHERE feed_id = '%s'" % (feedid))
    return c.fetchone()


def get_stats(c, player, data):
    c.execute(
        "SELECT id FROM wp_bp_teams_players_stats WHERE player_feed_id = '%s' AND season_feed_id = '%s' AND `type` = '%s' AND team_feed_id = '%s';" % (
        player.player_feed_id, player.season_feed_id, data.type, player.team_feed_id))
    return c.fetchone()


def insert_stats_basketball(c, player, data):
    if player.id:
        sql = """UPDATE wp_bp_teams_players_stats SET 
        type = '%s',
        games_played = %d,
        games_started = %d,
        seconds_played = %d,
        points = %d,
        points_highest = %d,
        field_goals_made = %d,
        field_goals_attempted = %d,
        three_point_field_goals_made = %d,
        three_point_field_goals_attempted = %d,
        free_throws_made = %d,
        free_throws_attempted = %d,
        plus_minus = %d,
        assists = %d,
        rebounds_offensive = %d,
        rebounds_defensive = %d,
        steals = %d,
        turnovers = %d,
        blocks = %d,
        fouls_personal = %d,
        fouls_technical = %d,
        player_feed_id = '%s',
        team_feed_id = '%s',
        season_feed_id = '%s',
        league_id = %d,
        season_name = '%s',
        player_id = %d 
        WHERE 
        id = %d
        ;""" % (
            data.type,
            data.games_played,
            data.games_started,
            data.seconds_played,
            data.points,
            data.points_highest,
            data.field_goals_made,
            data.field_goals_attempted,
            data.three_point_field_goals_made,
            data.three_point_field_goals_attempted,
            data.free_throws_made,
            data.free_throws_attempted,
            data.plus_minus,
            data.assists,
            data.rebounds_offensive,
            data.rebounds_defensive,
            data.steals,
            data.turnovers,
            data.blocks,
            data.fouls_personal,
            data.fouls_technical,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id,
            player.id
        )
    else:
        sql = """INSERT INTO wp_bp_teams_players_stats(
        type,
        games_played,
        games_started,
        seconds_played,
        points,
        points_highest,
        field_goals_made,
        field_goals_attempted,
        three_point_field_goals_made,
        three_point_field_goals_attempted,
        free_throws_made,
        free_throws_attempted,
        plus_minus,
        assists,
        rebounds_offensive,
        rebounds_defensive,
        steals,
        turnovers,
        blocks,
        fouls_personal,
        fouls_technical,
        player_feed_id,
        team_feed_id,
        season_feed_id,
        league_id,
        season_name,
        player_id
        ) VALUES (
        '%s',
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        %d,
        '%s',
        '%s',
        '%s',
        %d,
        '%s',
        %d
        );""" % (
            data.type,
            data.games_played,
            data.games_started,
            data.seconds_played,
            data.points,
            data.points_highest,
            data.field_goals_made,
            data.field_goals_attempted,
            data.three_point_field_goals_made,
            data.three_point_field_goals_attempted,
            data.free_throws_made,
            data.free_throws_attempted,
            data.plus_minus,
            data.assists,
            data.rebounds_offensive,
            data.rebounds_defensive,
            data.steals,
            data.turnovers,
            data.blocks,
            data.fouls_personal,
            data.fouls_technical,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id
        )
    print sql
    c.execute(sql)


def insert_stats_baseball(c, player, data):
    if player.id:
        sql = """UPDATE wp_bp_teams_players_stats SET
                    `type` = '%s',
                    `games_played` = %d,
                    `games_started` = %d,
                    `at_bats` = %d,
                    `runs` = %d,
                    `hits` = %d,
                    `doubles` = %d,
                    `triples` = %d,
                    `home_runs` = %d,
                    `total_bases` = %d,
                    `runs_batted_in` = %d,
                    `walks` = %d,
                    `intentional_walks` = %d,
                    `strikeouts` = %d,
                    `hit_by_pitch` = %d,
                    `stolen_bases` = %d,
                    `caught_stealing` = %d,
                    `sacrifice_hits` = %d,
                    `sacrifice_flys` = %d,
                    `grounded_into_double_plays` = %d,
                    `left_on_base` = %d,
                    `two_out_rbi` = %d,
                    `rlisp_two_out` = %d,
                    `slugging_percentage` = %f,
                    `on_base_percentage` = %f,
                    `batting_average` = %f,
                    `on_base_plus_slugging` = %f,
                    `fielding_errors` = %d,
                    `passed_balls` = %d,
                    `catcher_stealers_caught` = %d,
                    `catcher_stealers_allowed` = %d,
                    `catcher_interferences` = %d,
                    `outfield_assists` = %d,
                    `pitcher_games_played` = %d,
                    `pitcher_games_started` = %d,
                    `quality_starts` = %d,
                    `wins` = %d,
                    `losses` = %d,
                    `no_decisions` = %d,
                    `holds` = %d,
                    `saves` = %d,
                    `blown_saves` = %d,
                    `complete_games` = %d,
                    `shutouts` = %d,
                    `outs_pitched` = %d,
                    `earned_run_average` = %f,
                    `whip` = %f,
                    `pitcher_hits` = %d,
                    `pitcher_runs` = %d,
                    `pitcher_earned_runs` = %d,
                    `pitcher_walks` = %d,
                    `pitcher_strikeouts` = %d,
                    `pitcher_home_runs` = %d,
                    `pitcher_stolen_bases` = %d,
                    `pitcher_caught_stealing` = %d,
                    `pitcher_intentional_walks` = %d,
                    `pitcher_hit_by_pitch` = %d,
                    `pitcher_sacrifice_hits` = %d,
                    `pitcher_sacrifice_flys` = %d,
                    `pitches_thrown` = %d,
                    `starting_pitches_thrown` = %d,
                    `wild_pitches` = %d,
                    `strikes_thrown` = %d,
                    `ground_ball_outs` = %d,
                    `fly_ball_outs` = %d,
                    `batters_faced` = %d,
                    `pickoffs` = %d,
                    `inherited_runners` = %d,
                    `inherited_runners_scored` = %d,
                    `balks` = %d,
                    `player_feed_id` = '%s',
                    `team_feed_id` = '%s',
                    `season_feed_id` = '%s',
                    `league_id` = %d,
                    `season_name` = '%s',
                    `player_id` = %d
                    WHERE
                    `id` = %d
    """ % (
            data.type,
            data.games_played,
            data.games_started,
            data.at_bats,
            data.runs,
            data.hits,
            data.doubles,
            data.triples,
            data.home_runs,
            data.total_bases,
            data.runs_batted_in,
            data.walks,
            data.intentional_walks,
            data.strikeouts,
            data.hit_by_pitch,
            data.stolen_bases,
            data.caught_stealing,
            data.sacrifice_hits,
            data.sacrifice_flys,
            data.grounded_into_double_plays,
            data.left_on_base,
            data.two_out_rbi,
            data.rlisp_two_out,
            data.slugging_percentage,
            data.on_base_percentage,
            data.batting_average,
            data.on_base_plus_slugging,
            data.fielding_errors,
            data.passed_balls,
            data.catcher_stealers_caught,
            data.catcher_stealers_allowed,
            data.catcher_interferences,
            data.outfield_assists,
            data.pitcher_games_played,
            data.pitcher_games_started,
            data.quality_starts,
            data.wins,
            data.losses,
            data.no_decisions,
            data.holds,
            data.saves,
            data.blown_saves,
            data.complete_games,
            data.shutouts,
            data.outs_pitched,
            data.earned_run_average,
            data.whip,
            data.pitcher_hits,
            data.pitcher_runs,
            data.pitcher_earned_runs,
            data.pitcher_walks,
            data.pitcher_strikeouts,
            data.pitcher_home_runs,
            data.pitcher_stolen_bases,
            data.pitcher_caught_stealing,
            data.pitcher_intentional_walks,
            data.pitcher_hit_by_pitch,
            data.pitcher_sacrifice_hits,
            data.pitcher_sacrifice_flys,
            data.pitches_thrown,
            data.starting_pitches_thrown,
            data.wild_pitches,
            data.strikes_thrown,
            data.ground_ball_outs,
            data.fly_ball_outs,
            data.batters_faced,
            data.pickoffs,
            data.inherited_runners,
            data.inherited_runners_scored,
            data.balks,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id,
            player.id
        )
    else:
        sql = """INSERT INTO wp_bp_teams_players_stats (
                    `type`,
                    `games_played`,
                    `games_started`,
                    `at_bats`,
                    `runs`,
                    `hits`,
                    `doubles`,
                    `triples`,
                    `home_runs`,
                    `total_bases`,
                    `runs_batted_in`,
                    `walks`,
                    `intentional_walks`,
                    `strikeouts`,
                    `hit_by_pitch`,
                    `stolen_bases`,
                    `caught_stealing`,
                    `sacrifice_hits`,
                    `sacrifice_flys`,
                    `grounded_into_double_plays`,
                    `left_on_base`,
                    `two_out_rbi`,
                    `rlisp_two_out`,
                    `slugging_percentage`,
                    `on_base_percentage`,
                    `batting_average`,
                    `on_base_plus_slugging`,
                    `fielding_errors`,
                    `passed_balls`,
                    `catcher_stealers_caught`,
                    `catcher_stealers_allowed`,
                    `catcher_interferences`,
                    `outfield_assists`,
                    `pitcher_games_played`,
                    `pitcher_games_started`,
                    `quality_starts`,
                    `wins`,
                    `losses`,
                    `no_decisions`,
                    `holds`,
                    `saves`,
                    `blown_saves`,
                    `complete_games`,
                    `shutouts`,
                    `outs_pitched`,
                    `earned_run_average`,
                    `whip`,
                    `pitcher_hits`,
                    `pitcher_runs`,
                    `pitcher_earned_runs`,
                    `pitcher_walks`,
                    `pitcher_strikeouts`,
                    `pitcher_home_runs`,
                    `pitcher_stolen_bases`,
                    `pitcher_caught_stealing`,
                    `pitcher_intentional_walks`,
                    `pitcher_hit_by_pitch`,
                    `pitcher_sacrifice_hits`,
                    `pitcher_sacrifice_flys`,
                    `pitches_thrown`,
                    `starting_pitches_thrown`,
                    `wild_pitches`,
                    `strikes_thrown`,
                    `ground_ball_outs`,
                    `fly_ball_outs`,
                    `batters_faced`,
                    `pickoffs`,
                    `inherited_runners`,
                    `inherited_runners_scored`,
                    `balks`,
                    `player_feed_id`,
                    `team_feed_id`,
                    `season_feed_id`,
                    `league_id`,
                    `season_name`,
                    `player_id`
        ) VALUES (
                    '%s',
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %f,
                    %f,
                    %f,
                    %f,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %f,
                    %f,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    '%s',
                    '%s',
                    '%s',
                    %d,
                    '%s',
                    %d
        );
    """ % (
            data.type,
            data.games_played,
            data.games_started,
            data.at_bats,
            data.runs,
            data.hits,
            data.doubles,
            data.triples,
            data.home_runs,
            data.total_bases,
            data.runs_batted_in,
            data.walks,
            data.intentional_walks,
            data.strikeouts,
            data.hit_by_pitch,
            data.stolen_bases,
            data.caught_stealing,
            data.sacrifice_hits,
            data.sacrifice_flys,
            data.grounded_into_double_plays,
            data.left_on_base,
            data.two_out_rbi,
            data.rlisp_two_out,
            data.slugging_percentage,
            data.on_base_percentage,
            data.batting_average,
            data.on_base_plus_slugging,
            data.fielding_errors,
            data.passed_balls,
            data.catcher_stealers_caught,
            data.catcher_stealers_allowed,
            data.catcher_interferences,
            data.outfield_assists,
            data.pitcher_games_played,
            data.pitcher_games_started,
            data.quality_starts,
            data.wins,
            data.losses,
            data.no_decisions,
            data.holds,
            data.saves,
            data.blown_saves,
            data.complete_games,
            data.shutouts,
            data.outs_pitched,
            data.earned_run_average,
            data.whip,
            data.pitcher_hits,
            data.pitcher_runs,
            data.pitcher_earned_runs,
            data.pitcher_walks,
            data.pitcher_strikeouts,
            data.pitcher_home_runs,
            data.pitcher_stolen_bases,
            data.pitcher_caught_stealing,
            data.pitcher_intentional_walks,
            data.pitcher_hit_by_pitch,
            data.pitcher_sacrifice_hits,
            data.pitcher_sacrifice_flys,
            data.pitches_thrown,
            data.starting_pitches_thrown,
            data.wild_pitches,
            data.strikes_thrown,
            data.ground_ball_outs,
            data.fly_ball_outs,
            data.batters_faced,
            data.pickoffs,
            data.inherited_runners,
            data.inherited_runners_scored,
            data.balks,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id
        )

    print sql
    c.execute(sql)


def insert_stats_football(c, player, data):
    if player.id:
        sql = """UPDATE wp_bp_teams_players_stats SET
                    `type` = '%s',
                    `games_played` = %d,
                    `games_started` = %d,
                    `starter_games_won` = %d,
                    `starter_games_lost` = %d,
                    `starter_games_tied` =%d,
                    `passer_rating` = %f,
                    `rushing_plays` = %d,
                    `rushing_gross_yards` = %d,
                    `rushing_net_yards` = %d,
                    `rushing_lost_yards` = %d,
                    `rushing_longest_yards` = %d,
                    `rushing_touchdowns` = %d,
                    `rushing_touchdowns_longest_yards` = %d,
                    `rushing_2pt_conversions_succeeded` = %d,
                    `passing_plays_attempted` = %d,
                    `passing_plays_completed` = %d,
                    `passing_gross_yards` = %d,
                    `passing_net_yards` = %d,
                    `passing_longest_yards` = %d,
                    `passing_plays_intercepted` = %d,
                    `passing_plays_sacked` = %d,
                    `passing_sacked_yards` = %d,
                    `passing_touchdowns` = %d,
                    `passing_touchdowns_longest_yards` = %d,
                    `passing_2pt_conversions_succeeded` = %d,
                    `receiving_targeted` = %d,
                    `receiving_receptions` = %d,
                    `receiving_yards` = %d,
                    `receiving_longest_yards` = %d,
                    `receiving_touchdowns` = %d,
                    `receiving_touchdowns_longest_yards` = %d,
                    `receiving_2pt_conversions_succeeded` = %d,
                    `fumbles` = %d,
                    `fumbles_lost` = %d,
                    `fumbles_recovered_lost_by_opposition` = %d,
                    `fumbles_recovered_touchdowns` = %d,
                    `fumbles_recovered_touchdowns_longest_yards` = %d,
                    `interceptions_returned_touchdowns` = %d,
                    `interceptions_returned_touchdowns_longest_yards` = %d,
                    `punting_plays` = %d,
                    `punting_gross_yards` = %d,
                    `punting_net_yards` = %d,
                    `punting_touchbacks` = %d,
                    `punting_singles` = %d,
                    `punting_inside_twenty` = %d,
                    `punting_longest_yards` = %d,
                    `punt_returns` = %d,
                    `punt_return_yards` = %d,
                    `punt_return_longest_yards` = %d,
                    `punt_return_faircatches` = %d,
                    `punt_return_touchdowns` = %d,
                    `punt_return_touchdowns_longest_yards` = %d,
                    `kickoffs` = %d,
                    `kickoff_yards` = %d,
                    `kickoff_longest_yards` = %d,
                    `kickoff_singles` = %d,
                    `kickoff_returns` = %d,
                    `kickoff_return_yards` = %d,
                    `kickoff_return_longest_yards` = %d,
                    `kickoff_return_faircatches` = %d,
                    `kickoff_return_touchdowns` = %d,
                    `kickoff_return_touchdowns_longest_yards` = %d,
                    `extra_point_kicks_attempted` = %d,
                    `extra_point_kicks_succeeded` = %d,
                    `field_goals_attempted` = %d,
                    `field_goals_succeeded` = %d,
                    `field_goals_succeeded_yards` = %d,
                    `field_goals_succeeded_longest_yards` = %d,
                    `field_goals_blocked` = %d,
                    `kicking_singles` = %d,
                    `defense_interceptions` = %d,
                    `defense_interception_yards` = %f,
                    `defense_tackles` = %f,
                    `defense_solo_tackles` = %d,
                    `defense_assisted_tackles` = %d,
                    `defense_special_teams_tackles` = %d,
                    `defense_special_teams_solo_tackles` = %d,
                    `defense_special_teams_assisted_tackles` = %d,
                    `defense_misc_solo_tackles` = %d,
                    `defense_misc_assisted_tackles` = %d,
                    `defense_sacks` = %d,
                    `defense_sack_yards` = %d,
                    `defense_tackles_for_loss` = %f,
                    `defense_tackles_for_loss_yards` = %f,
                    `defense_forced_fumbles` = %d,
                    `defense_fumble_recoveries` = %d,
                    `defense_special_teams_fumble_recoveries` = %d,
                    `defense_miscellaneous_fumble_recoveries` = %d,
                    `defense_pass_defenses` = %d,
                    `penalty_yards` = %d,
                    `total_touchdowns` = %d,
                    `player_feed_id` = '%s',
                    `team_feed_id` = '%s',
                    `season_feed_id` = '%s',
                    `league_id` = %d,
                    `season_name` = '%s',
                    `player_id` = %d
                    WHERE 
                    `id` = %d
            ;
        """ % (
            data.type,
            data.games_played,
            data.games_started,
            data.starter_games_won,
            data.starter_games_lost,
            data.starter_games_tied,
            data.passer_rating,
            data.rushing_plays,
            data.rushing_gross_yards,
            data.rushing_net_yards,
            data.rushing_lost_yards,
            data.rushing_longest_yards,
            data.rushing_touchdowns,
            data.rushing_touchdowns_longest_yards,
            data.rushing_2pt_conversions_succeeded,
            data.passing_plays_attempted,
            data.passing_plays_completed,
            data.passing_gross_yards,
            data.passing_net_yards,
            data.passing_longest_yards,
            data.passing_plays_intercepted,
            data.passing_plays_sacked,
            data.passing_sacked_yards,
            data.passing_touchdowns,
            data.passing_touchdowns_longest_yards,
            data.passing_2pt_conversions_succeeded,
            data.receiving_targeted,
            data.receiving_receptions,
            data.receiving_yards,
            data.receiving_longest_yards,
            data.receiving_touchdowns,
            data.receiving_touchdowns_longest_yards,
            data.receiving_2pt_conversions_succeeded,
            data.fumbles,
            data.fumbles_lost,
            data.fumbles_recovered_lost_by_opposition,
            data.fumbles_recovered_touchdowns,
            data.fumbles_recovered_touchdowns_longest_yards,
            data.interceptions_returned_touchdowns,
            data.interceptions_returned_touchdowns_longest_yards,
            data.punting_plays,
            data.punting_gross_yards,
            data.punting_net_yards,
            data.punting_touchbacks,
            data.punting_singles,
            data.punting_inside_twenty,
            data.punting_longest_yards,
            data.punt_returns,
            data.punt_return_yards,
            data.punt_return_longest_yards,
            data.punt_return_faircatches,
            data.punt_return_touchdowns,
            data.punt_return_touchdowns_longest_yards,
            data.kickoffs,
            data.kickoff_yards,
            data.kickoff_longest_yards,
            data.kickoff_singles,
            data.kickoff_returns,
            data.kickoff_return_yards,
            data.kickoff_return_longest_yards,
            data.kickoff_return_faircatches,
            data.kickoff_return_touchdowns,
            data.kickoff_return_touchdowns_longest_yards,
            data.extra_point_kicks_attempted,
            data.extra_point_kicks_succeeded,
            data.field_goals_attempted,
            data.field_goals_succeeded,
            data.field_goals_succeeded_yards,
            data.field_goals_succeeded_longest_yards,
            data.field_goals_blocked,
            data.kicking_singles,
            data.defense_interceptions,
            data.defense_interception_yards,
            data.defense_tackles,
            data.defense_solo_tackles,
            data.defense_assisted_tackles,
            data.defense_special_teams_tackles,
            data.defense_special_teams_solo_tackles,
            data.defense_special_teams_assisted_tackles,
            data.defense_misc_solo_tackles,
            data.defense_misc_assisted_tackles,
            data.defense_sacks,
            data.defense_sack_yards,
            data.defense_tackles_for_loss,
            data.defense_tackles_for_loss_yards,
            data.defense_forced_fumbles,
            data.defense_fumble_recoveries,
            data.defense_special_teams_fumble_recoveries,
            data.defense_miscellaneous_fumble_recoveries,
            data.defense_pass_defenses,
            data.penalty_yards,
            data.total_touchdowns,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id,
            player.id
        )
    else:
        sql = """INSERT INTO wp_bp_teams_players_stats (
                    `type`,
                    `games_played`,
                    `games_started`,
                    `starter_games_won`,
                    `starter_games_lost`,
                    `starter_games_tied`,
                    `passer_rating`,
                    `rushing_plays`,
                    `rushing_gross_yards`,
                    `rushing_net_yards`,
                    `rushing_lost_yards`,
                    `rushing_longest_yards`,
                    `rushing_touchdowns`,
                    `rushing_touchdowns_longest_yards`,
                    `rushing_2pt_conversions_succeeded`,
                    `passing_plays_attempted`,
                    `passing_plays_completed`,
                    `passing_gross_yards`,
                    `passing_net_yards`,
                    `passing_longest_yards`,
                    `passing_plays_intercepted`,
                    `passing_plays_sacked`,
                    `passing_sacked_yards`,
                    `passing_touchdowns`,
                    `passing_touchdowns_longest_yards`,
                    `passing_2pt_conversions_succeeded`,
                    `receiving_targeted`,
                    `receiving_receptions`,
                    `receiving_yards`,
                    `receiving_longest_yards`,
                    `receiving_touchdowns`,
                    `receiving_touchdowns_longest_yards`,
                    `receiving_2pt_conversions_succeeded`,
                    `fumbles`,
                    `fumbles_lost`,
                    `fumbles_recovered_lost_by_opposition`,
                    `fumbles_recovered_touchdowns`,
                    `fumbles_recovered_touchdowns_longest_yards`,
                    `interceptions_returned_touchdowns`,
                    `interceptions_returned_touchdowns_longest_yards`,
                    `punting_plays`,
                    `punting_gross_yards`,
                    `punting_net_yards`,
                    `punting_touchbacks`,
                    `punting_singles`,
                    `punting_inside_twenty`,
                    `punting_longest_yards`,
                    `punt_returns`,
                    `punt_return_yards`,
                    `punt_return_longest_yards`,
                    `punt_return_faircatches`,
                    `punt_return_touchdowns`,
                    `punt_return_touchdowns_longest_yards`,
                    `kickoffs`,
                    `kickoff_yards`,
                    `kickoff_longest_yards`,
                    `kickoff_singles`,
                    `kickoff_returns`,
                    `kickoff_return_yards`,
                    `kickoff_return_longest_yards`,
                    `kickoff_return_faircatches`,
                    `kickoff_return_touchdowns`,
                    `kickoff_return_touchdowns_longest_yards`,
                    `extra_point_kicks_attempted`,
                    `extra_point_kicks_succeeded`,
                    `field_goals_attempted`,
                    `field_goals_succeeded`,
                    `field_goals_succeeded_yards`,
                    `field_goals_succeeded_longest_yards`,
                    `field_goals_blocked`,
                    `kicking_singles`,
                    `defense_interceptions`,
                    `defense_interception_yards`,
                    `defense_tackles`,
                    `defense_solo_tackles`,
                    `defense_assisted_tackles`,
                    `defense_special_teams_tackles`,
                    `defense_special_teams_solo_tackles`,
                    `defense_special_teams_assisted_tackles`,
                    `defense_misc_solo_tackles`,
                    `defense_misc_assisted_tackles`,
                    `defense_sacks`,
                    `defense_sack_yards`,
                    `defense_tackles_for_loss`,
                    `defense_tackles_for_loss_yards`,
                    `defense_forced_fumbles`,
                    `defense_fumble_recoveries`,
                    `defense_special_teams_fumble_recoveries`,
                    `defense_miscellaneous_fumble_recoveries`,
                    `defense_pass_defenses`,
                    `penalty_yards`,
                    `total_touchdowns`,
                    `player_feed_id`,
                    `team_feed_id`,
                    `season_feed_id`,
                    `league_id`,
                    `season_name`,
                    `player_id`
        ) VALUES (
                    '%s',
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %f,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %f,
                    %f,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %f,
                    %f,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    '%s',
                    '%s',
                    '%s',
                    %d,
                    '%s',
                    %d
        );
    """ % (
            data.type,
            data.games_played,
            data.games_started,
            data.starter_games_won,
            data.starter_games_lost,
            data.starter_games_tied,
            data.passer_rating,
            data.rushing_plays,
            data.rushing_gross_yards,
            data.rushing_net_yards,
            data.rushing_lost_yards,
            data.rushing_longest_yards,
            data.rushing_touchdowns,
            data.rushing_touchdowns_longest_yards,
            data.rushing_2pt_conversions_succeeded,
            data.passing_plays_attempted,
            data.passing_plays_completed,
            data.passing_gross_yards,
            data.passing_net_yards,
            data.passing_longest_yards,
            data.passing_plays_intercepted,
            data.passing_plays_sacked,
            data.passing_sacked_yards,
            data.passing_touchdowns,
            data.passing_touchdowns_longest_yards,
            data.passing_2pt_conversions_succeeded,
            data.receiving_targeted,
            data.receiving_receptions,
            data.receiving_yards,
            data.receiving_longest_yards,
            data.receiving_touchdowns,
            data.receiving_touchdowns_longest_yards,
            data.receiving_2pt_conversions_succeeded,
            data.fumbles,
            data.fumbles_lost,
            data.fumbles_recovered_lost_by_opposition,
            data.fumbles_recovered_touchdowns,
            data.fumbles_recovered_touchdowns_longest_yards,
            data.interceptions_returned_touchdowns,
            data.interceptions_returned_touchdowns_longest_yards,
            data.punting_plays,
            data.punting_gross_yards,
            data.punting_net_yards,
            data.punting_touchbacks,
            data.punting_singles,
            data.punting_inside_twenty,
            data.punting_longest_yards,
            data.punt_returns,
            data.punt_return_yards,
            data.punt_return_longest_yards,
            data.punt_return_faircatches,
            data.punt_return_touchdowns,
            data.punt_return_touchdowns_longest_yards,
            data.kickoffs,
            data.kickoff_yards,
            data.kickoff_longest_yards,
            data.kickoff_singles,
            data.kickoff_returns,
            data.kickoff_return_yards,
            data.kickoff_return_longest_yards,
            data.kickoff_return_faircatches,
            data.kickoff_return_touchdowns,
            data.kickoff_return_touchdowns_longest_yards,
            data.extra_point_kicks_attempted,
            data.extra_point_kicks_succeeded,
            data.field_goals_attempted,
            data.field_goals_succeeded,
            data.field_goals_succeeded_yards,
            data.field_goals_succeeded_longest_yards,
            data.field_goals_blocked,
            data.kicking_singles,
            data.defense_interceptions,
            data.defense_interception_yards,
            data.defense_tackles,
            data.defense_solo_tackles,
            data.defense_assisted_tackles,
            data.defense_special_teams_tackles,
            data.defense_special_teams_solo_tackles,
            data.defense_special_teams_assisted_tackles,
            data.defense_misc_solo_tackles,
            data.defense_misc_assisted_tackles,
            data.defense_sacks,
            data.defense_sack_yards,
            data.defense_tackles_for_loss,
            data.defense_tackles_for_loss_yards,
            data.defense_forced_fumbles,
            data.defense_fumble_recoveries,
            data.defense_special_teams_fumble_recoveries,
            data.defense_miscellaneous_fumble_recoveries,
            data.defense_pass_defenses,
            data.penalty_yards,
            data.total_touchdowns,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id
        )

        print sql
    c.execute(sql)


def insert_stats_hockey(c, player, data):
    if player.id:
        sql = """UPDATE wp_bp_teams_players_stats SET 
                    `type` = '%s',
                    `games_played` = %d,
                    `goals` = %d,
                    `goals_period_1` = %d,
                    `goals_period_2` = %d,
                    `goals_period_3` = %d,
                    `goals_overtime` = %d,
                    `goals_power_play` = %d,
                    `goals_short_handed` = %d,
                    `game_winning_goals` = %d,
                    `assists` = %d,
                    `plus_minus` = %d,
                    `penalty_minutes` = %d,
                    `shots` = %d,
                    `faceoffs_won` = %d,
                    `faceoffs_lost` = %d,
                    `time_on_ice_secs` = %d,
                    `time_on_ice_even_strength_secs` = %d,
                    `time_on_ice_power_play_secs` = %d,
                    `time_on_ice_short_handed_secs` = %d,
                    `shifts` = %d,
                    `player_feed_id` = '%s',
                    `team_feed_id` = '%s',
                    `season_feed_id` = '%s',
                    `league_id` = %d,
                    `season_name` = '%s',
                    `player_id` = %d
                    WHERE
                    `id` = %d
        ;""" % (
            data.type,
            data.games_played,
            data.goals,
            data.goals_period_1,
            data.goals_period_2,
            data.goals_period_3,
            data.goals_overtime,
            data.goals_power_play,
            data.goals_short_handed,
            data.game_winning_goals,
            data.assists,
            data.plus_minus,
            data.penalty_minutes,
            data.shots,
            data.faceoffs_won,
            data.faceoffs_lost,
            data.time_on_ice_secs,
            data.time_on_ice_even_strength_secs,
            data.time_on_ice_power_play_secs,
            data.time_on_ice_short_handed_secs,
            data.shifts,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id,
            player.id
        )
    else:
        sql = """INSERT INTO wp_bp_teams_players_stats (
                    `type`,
                    `games_played`,
                    `goals`,
                    `goals_period_1`,
                    `goals_period_2`,
                    `goals_period_3`,
                    `goals_overtime`,
                    `goals_power_play`,
                    `goals_short_handed`,
                    `game_winning_goals`,
                    `assists`,
                    `plus_minus`,
                    `penalty_minutes`,
                    `shots`,
                    `faceoffs_won`,
                    `faceoffs_lost`,
                    `time_on_ice_secs`,
                    `time_on_ice_even_strength_secs`,
                    `time_on_ice_power_play_secs`,
                    `time_on_ice_short_handed_secs`,
                    `shifts`,
                    `player_feed_id`,
                    `team_feed_id`,
                    `season_feed_id`,
                    `league_id`,
                    `season_name`,
                    `player_id`
        ) VALUES (
                    '%s',
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    '%s',
                    '%s',
                    '%s',
                    %d,
                    '%s',
                    %d
        );""" % (
            data.type,
            data.games_played,
            data.goals,
            data.goals_period_1,
            data.goals_period_2,
            data.goals_period_3,
            data.goals_overtime,
            data.goals_power_play,
            data.goals_short_handed,
            data.game_winning_goals,
            data.assists,
            data.plus_minus,
            data.penalty_minutes,
            data.shots,
            data.faceoffs_won,
            data.faceoffs_lost,
            data.time_on_ice_secs,
            data.time_on_ice_even_strength_secs,
            data.time_on_ice_power_play_secs,
            data.time_on_ice_short_handed_secs,
            data.shifts,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id
        )
    print sql
    c.execute(sql)


def insert_stats_soccer(c, player, data):
    if player.id:
        sql = """UPDATE wp_bp_teams_players_stats SET 
                    `type` = '%s',
                    `goals` = %d,
                    `goals_half_1` = %d,
                    `goals_half_2` = %d,
                    `goals_penalty` = %d,
                    `goals_scored_first` = %d,
                    `own_goals` = %d,
                    `yellow_cards` = %d,
                    `red_cards` = %d,
                    `discipline_points` = %d,
                    `player_feed_id` = '%s',
                    `team_feed_id` = '%s',
                    `season_feed_id` = '%s',
                    `league_id` = %d,
                    `season_name` = '%s',
                    `player_id` = %d
                    WHERE
                    `id` = %d
        ;""" % (
            data.type,
            data.goals,
            data.goals_half_1,
            data.goals_half_2,
            data.goals_penalty,
            data.goals_scored_first,
            data.own_goals,
            data.yellow_cards,
            data.red_cards,
            data.discipline_points,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id,
            player.id
        )
    else:
        sql = """INSERT INTO wp_bp_teams_players_stats (
                    `type`,
                    `goals`,
                    `goals_half_1`,
                    `goals_half_2`,
                    `goals_penalty`,
                    `goals_scored_first`,
                    `own_goals`,
                    `yellow_cards`,
                    `red_cards`,
                    `discipline_points`,
                    `player_feed_id`,
                    `team_feed_id`,
                    `season_feed_id`,
                    `league_id`,
                    `season_name`,
                    `player_id`
        ) VALUES (
                    '%s',
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    '%s',
                    '%s',
                    '%s',
                    %d,
                    '%s',
                    %d
        );""" % (
            data.type,
            data.goals,
            data.goals_half_1,
            data.goals_half_2,
            data.goals_penalty,
            data.goals_scored_first,
            data.own_goals,
            data.yellow_cards,
            data.red_cards,
            data.discipline_points,
            player.player_feed_id,
            player.team_feed_id,
            player.season_feed_id,
            player.league_id,
            player.season_name,
            player.player_id
        )
    print sql
    c.execute(sql)


# Calculating the current datetime minus 1 day
from datetime import datetime, timedelta

currdate = datetime.today() - timedelta(days=1)

d = feedparser.parse(
    "http://xml.sportsdirectinc.com/Atom?feed=/" + sport + "/" + screen + "&newerThan=" + currdate.strftime(
        "%Y-%m-%dT%H:%M:%S"))
# d = feedparser.parse("http://xml.sportsdirectinc.com/Atom?feed=/"+sport+"/"+screen+"&newerThan="+(date.today()-timedelta(days = 1)).isoformat()+"T12:42:13")
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
        for xseason in soup.findAll('season'):
            season_feed_id = xseason.contents[0].string
            season_name = xseason.contents[1].string
            lid = get_league(c, league)
            league_id = int(lid[0])
        for xteamcontent in soup.findAll('team-content'):
            player = PlayerStats()
            for xteam in soup.findAll('team'):
                team_feed_id = xteam.contents[0].string
                player.team_feed_id = team_feed_id
                player.season_feed_id = season_feed_id
                player.league_id = league_id
                player.season_name = season_name
            for xplayercontent in xteamcontent.findAll('player-content'):
                player.player_feed_id = xplayercontent.contents[0].contents[0].string
                pid = get_player(c, player.player_feed_id)
                if pid is None:
                    print 'no player'
                    continue
                player.player_id = int(pid[0] or 0)
                for xstatgroup in xplayercontent.findAll('stat-group'):
                    stats = {}
                    for xstat in xstatgroup.findAll('stat'):
                        stats[xstat.get('type')] = xstat.get('num')
                    if sport == 'basketball':
                        data = StatsBasketball()
                        data.type = xstatgroup.contents[0].string
                        data.games_played = int(stats.get('games_played') or 0)
                        data.games_started = int(stats.get('games_started') or 0)
                        data.seconds_played = int(stats.get('seconds_played') or 0)
                        data.points = int(stats.get('points') or 0)
                        data.points_highest = int(stats.get('points_highest') or 0)
                        data.field_goals_made = int(stats.get('field_goals_made') or 0)
                        data.field_goals_attempted = int(stats.get('field_goals_attempted') or 0)
                        data.three_point_field_goals_made = int(stats.get('three_point_field_goals_made') or 0)
                        data.three_point_field_goals_attempted = int(
                            stats.get('three_point_field_goals_attempted') or 0)
                        data.free_throws_made = int(stats.get('free_throws_made') or 0)
                        data.free_throws_attempted = int(stats.get('free_throws_attempted') or 0)
                        data.plus_minus = int(stats.get('plus_minus') or 0)
                        data.assists = int(stats.get('assists') or 0)
                        data.rebounds_offensive = int(stats.get('rebounds_offensive') or 0)
                        data.rebounds_defensive = int(stats.get('rebounds_defensive') or 0)
                        data.steals = int(stats.get('steals') or 0)
                        data.turnovers = int(stats.get('turnovers') or 0)
                        data.blocks = int(stats.get('blocks') or 0)
                        data.fouls_personal = int(stats.get('fouls_personal') or 0)
                        data.fouls_technical = int(stats.get('fouls_technical') or 0)
                        sid = get_stats(c, player, data)
                        if sid is not None:
                            player.id = int(sid[0])
                        insert_stats_basketball(c, player, data)
                    if sport == 'baseball':
                        data = StatsBaseball()
                        data.type = xstatgroup.contents[0].string
                        data.games_played = int(stats.get('games_played') or 0)
                        data.games_started = int(stats.get('games_started') or 0)
                        data.at_bats = int(stats.get('at_bats') or 0)
                        data.runs = int(stats.get('runs') or 0)
                        data.hits = int(stats.get('hits') or 0)
                        data.doubles = int(stats.get('doubles') or 0)
                        data.triples = int(stats.get('triples') or 0)
                        data.home_runs = int(stats.get('home_runs') or 0)
                        data.total_bases = int(stats.get('total_bases') or 0)
                        data.runs_batted_in = int(stats.get('runs_batted_in') or 0)
                        data.walks = int(stats.get('walks') or 0)
                        data.intentional_walks = int(stats.get('intentional_walks') or 0)
                        data.strikeouts = int(stats.get('strikeouts') or 0)
                        data.hit_by_pitch = int(stats.get('hit_by_pitch') or 0)
                        data.stolen_bases = int(stats.get('stolen_bases') or 0)
                        data.caught_stealing = int(stats.get('caught_stealing') or 0)
                        data.sacrifice_hits = int(stats.get('sacrifice_hits') or 0)
                        data.sacrifice_flys = int(stats.get('sacrifice_flys') or 0)
                        data.grounded_into_double_plays = int(stats.get('grounded_into_double_plays') or 0)
                        data.left_on_base = int(stats.get('left_on_base') or 0)
                        data.two_out_rbi = int(stats.get('two_out_rbi') or 0)
                        data.rlisp_two_out = int(stats.get('rlisp_two_out') or 0)
                        data.slugging_percentage = float(stats.get('slugging_percentage') or 0)
                        data.on_base_percentage = float(stats.get('on_base_percentage') or 0)
                        data.batting_average = float(stats.get('batting_average') or 0)
                        data.on_base_plus_slugging = float(stats.get('on_base_plus_slugging') or 0)
                        data.fielding_errors = int(stats.get('fielding_errors') or 0)
                        data.passed_balls = int(stats.get('passed_balls') or 0)
                        data.catcher_stealers_caught = int(stats.get('catcher_stealers_caught') or 0)
                        data.catcher_stealers_allowed = int(stats.get('catcher_stealers_allowed') or 0)
                        data.catcher_interferences = int(stats.get('catcher_interferences') or 0)
                        data.outfield_assists = int(stats.get('outfield_assists') or 0)
                        data.pitcher_games_played = int(stats.get('pitcher_games_played') or 0)
                        data.pitcher_games_started = int(stats.get('pitcher_games_started') or 0)
                        data.quality_starts = int(stats.get('quality_starts') or 0)
                        data.wins = int(stats.get('wins') or 0)
                        data.losses = int(stats.get('losses') or 0)
                        data.no_decisions = int(stats.get('no_decisions') or 0)
                        data.holds = int(stats.get('holds') or 0)
                        data.saves = int(stats.get('saves') or 0)
                        data.blown_saves = int(stats.get('blown_saves') or 0)
                        data.complete_games = int(stats.get('complete_games') or 0)
                        data.shutouts = int(stats.get('shutouts') or 0)
                        data.outs_pitched = int(stats.get('outs_pitched') or 0)
                        data.earned_run_average = float(stats.get('earned_run_average') or 0)
                        data.whip = float(stats.get('whip') or 0)
                        data.pitcher_hits = int(stats.get('pitcher_hits') or 0)
                        data.pitcher_runs = int(stats.get('pitcher_runs') or 0)
                        data.pitcher_earned_runs = int(stats.get('pitcher_earned_runs') or 0)
                        data.pitcher_walks = int(stats.get('pitcher_walks') or 0)
                        data.pitcher_strikeouts = int(stats.get('pitcher_strikeouts') or 0)
                        data.pitcher_home_runs = int(stats.get('pitcher_home_runs') or 0)
                        data.pitcher_stolen_bases = int(stats.get('pitcher_stolen_bases') or 0)
                        data.pitcher_caught_stealing = int(stats.get('pitcher_caught_stealing') or 0)
                        data.pitcher_intentional_walks = int(stats.get('pitcher_intentional_walks') or 0)
                        data.pitcher_hit_by_pitch = int(stats.get('pitcher_hit_by_pitch') or 0)
                        data.pitcher_sacrifice_hits = int(stats.get('pitcher_sacrifice_hits') or 0)
                        data.pitcher_sacrifice_flys = int(stats.get('pitcher_sacrifice_flys') or 0)
                        data.pitches_thrown = int(stats.get('pitches_thrown') or 0)
                        data.starting_pitches_thrown = int(stats.get('starting_pitches_thrown') or 0)
                        data.wild_pitches = int(stats.get('wild_pitches') or 0)
                        data.strikes_thrown = int(stats.get('strikes_thrown') or 0)
                        data.ground_ball_outs = int(stats.get('ground_ball_outs') or 0)
                        data.fly_ball_outs = int(stats.get('fly_ball_outs') or 0)
                        data.batters_faced = int(stats.get('batters_faced') or 0)
                        data.pickoffs = int(stats.get('pickoffs') or 0)
                        data.inherited_runners = int(stats.get('inherited_runners') or 0)
                        data.inherited_runners_scored = int(stats.get('inherited_runners_scored') or 0)
                        data.balks = int(stats.get('balks') or 0)
                        sid = get_stats(c, player, data)
                        if sid is not None:
                            player.id = int(sid[0])
                        insert_stats_baseball(c, player, data)
                    if sport == 'football':
                        data = StatsFootball()
                        data.type = xstatgroup.contents[0].string
                        data.games_played = int(stats.get('games_played') or 0)
                        data.games_started = int(stats.get('games_started') or 0)
                        data.starter_games_won = int(stats.get('starter_games_won') or 0)
                        data.starter_games_lost = int(stats.get('starter_games_lost') or 0)
                        data.starter_games_tied = int(stats.get('starter_games_tied') or 0)
                        data.passer_rating = float(stats.get('passer_rating') or 0)
                        data.rushing_plays = int(stats.get('rushing_plays') or 0)
                        data.rushing_gross_yards = int(stats.get('rushing_gross_yards') or 0)
                        data.rushing_net_yards = int(stats.get('rushing_net_yards') or 0)
                        data.rushing_lost_yards = int(stats.get('rushing_lost_yards') or 0)
                        data.rushing_longest_yards = int(stats.get('rushing_longest_yards') or 0)
                        data.rushing_touchdowns = int(stats.get('rushing_touchdowns') or 0)
                        data.rushing_touchdowns_longest_yards = int(stats.get('rushing_touchdowns_longest_yards') or 0)
                        data.rushing_2pt_conversions_succeeded = int(
                            stats.get('rushing_2pt_conversions_succeeded') or 0)
                        data.passing_plays_attempted = int(stats.get('passing_plays_attempted') or 0)
                        data.passing_plays_completed = int(stats.get('passing_plays_completed') or 0)
                        data.passing_gross_yards = int(stats.get('passing_gross_yards') or 0)
                        data.passing_net_yards = int(stats.get('passing_net_yards') or 0)
                        data.passing_longest_yards = int(stats.get('passing_longest_yards') or 0)
                        data.passing_plays_intercepted = int(stats.get('passing_plays_intercepted') or 0)
                        data.passing_plays_sacked = int(stats.get('passing_plays_sacked') or 0)
                        data.passing_sacked_yards = int(stats.get('passing_sacked_yards') or 0)
                        data.passing_touchdowns = int(stats.get('passing_touchdowns') or 0)
                        data.passing_touchdowns_longest_yards = int(stats.get('passing_touchdowns_longest_yards') or 0)
                        data.passing_2pt_conversions_succeeded = int(
                            stats.get('passing_2pt_conversions_succeeded') or 0)
                        data.receiving_targeted = int(stats.get('receiving_targeted') or 0)
                        data.receiving_receptions = int(stats.get('receiving_receptions') or 0)
                        data.receiving_yards = int(stats.get('receiving_yards') or 0)
                        data.receiving_longest_yards = int(stats.get('receiving_longest_yards') or 0)
                        data.receiving_touchdowns = int(stats.get('receiving_touchdowns') or 0)
                        data.receiving_touchdowns_longest_yards = int(
                            stats.get('receiving_touchdowns_longest_yards') or 0)
                        data.receiving_2pt_conversions_succeeded = int(
                            stats.get('receiving_2pt_conversions_succeeded') or 0)
                        data.fumbles = int(stats.get('fumbles') or 0)
                        data.fumbles_lost = int(stats.get('fumbles_lost') or 0)
                        data.fumbles_recovered_lost_by_opposition = int(
                            stats.get('fumbles_recovered_lost_by_opposition') or 0)
                        data.fumbles_recovered_touchdowns = int(stats.get('fumbles_recovered_touchdowns') or 0)
                        data.fumbles_recovered_touchdowns_longest_yards = int(
                            stats.get('fumbles_recovered_touchdowns_longest_yards') or 0)
                        data.interceptions_returned_touchdowns = int(
                            stats.get('interceptions_returned_touchdowns') or 0)
                        data.interceptions_returned_touchdowns_longest_yards = int(
                            stats.get('interceptions_returned_touchdowns_longest_yards') or 0)
                        data.punting_plays = int(stats.get('punting_plays') or 0)
                        data.punting_gross_yards = int(stats.get('punting_gross_yards') or 0)
                        data.punting_net_yards = int(stats.get('punting_net_yards') or 0)
                        data.punting_touchbacks = int(stats.get('punting_touchbacks') or 0)
                        data.punting_singles = int(stats.get('punting_singles') or 0)
                        data.punting_inside_twenty = int(stats.get('punting_inside_twenty') or 0)
                        data.punting_longest_yards = int(stats.get('punting_longest_yards') or 0)
                        data.punt_returns = int(stats.get('punt_returns') or 0)
                        data.punt_return_yards = int(stats.get('punt_return_yards') or 0)
                        data.punt_return_longest_yards = int(stats.get('punt_return_longest_yards') or 0)
                        data.punt_return_faircatches = int(stats.get('punt_return_faircatches') or 0)
                        data.punt_return_touchdowns = int(stats.get('punt_return_touchdowns') or 0)
                        data.punt_return_touchdowns_longest_yards = int(
                            stats.get('punt_return_touchdowns_longest_yards') or 0)
                        data.kickoffs = int(stats.get('kickoffs') or 0)
                        data.kickoff_yards = int(stats.get('kickoff_yards') or 0)
                        data.kickoff_longest_yards = int(stats.get('kickoff_longest_yards') or 0)
                        data.kickoff_singles = int(stats.get('kickoff_singles') or 0)
                        data.kickoff_returns = int(stats.get('kickoff_returns') or 0)
                        data.kickoff_return_yards = int(stats.get('kickoff_return_yards') or 0)
                        data.kickoff_return_longest_yards = int(stats.get('kickoff_return_longest_yards') or 0)
                        data.kickoff_return_faircatches = int(stats.get('kickoff_return_faircatches') or 0)
                        data.kickoff_return_touchdowns = int(stats.get('kickoff_return_touchdowns') or 0)
                        data.kickoff_return_touchdowns_longest_yards = int(
                            stats.get('kickoff_return_touchdowns_longest_yards') or 0)
                        data.extra_point_kicks_attempted = int(stats.get('extra_point_kicks_attempted') or 0)
                        data.extra_point_kicks_succeeded = int(stats.get('extra_point_kicks_succeeded') or 0)
                        data.field_goals_attempted = int(stats.get('field_goals_attempted') or 0)
                        data.field_goals_succeeded = int(stats.get('field_goals_succeeded') or 0)
                        data.field_goals_succeeded_yards = int(stats.get('field_goals_succeeded_yards') or 0)
                        data.field_goals_succeeded_longest_yards = int(
                            stats.get('field_goals_succeeded_longest_yards') or 0)
                        data.field_goals_blocked = int(stats.get('field_goals_blocked') or 0)
                        data.kicking_singles = int(stats.get('kicking_singles') or 0)
                        data.defense_interceptions = int(stats.get('defense_interceptions') or 0)
                        data.defense_interception_yards = int(stats.get('defense_interception_yards') or 0)
                        data.defense_tackles = int(stats.get('defense_tackles') or 0)
                        data.defense_solo_tackles = int(stats.get('defense_solo_tackles') or 0)
                        data.defense_assisted_tackles = int(stats.get('defense_assisted_tackles') or 0)
                        data.defense_special_teams_tackles = int(stats.get('defense_special_teams_tackles') or 0)
                        data.defense_special_teams_solo_tackles = int(
                            stats.get('defense_special_teams_solo_tackles') or 0)
                        data.defense_special_teams_assisted_tackles = int(
                            stats.get('defense_special_teams_assisted_tackles') or 0)
                        data.defense_misc_solo_tackles = int(stats.get('defense_misc_solo_tackles') or 0)
                        data.defense_misc_assisted_tackles = int(stats.get('defense_misc_assisted_tackles') or 0)
                        data.defense_sacks = float(stats.get('defense_sacks') or 0)
                        data.defense_sack_yards = float(stats.get('defense_sack_yards') or 0)
                        data.defense_tackles_for_loss = float(stats.get('defense_tackles_for_loss') or 0)
                        data.defense_tackles_for_loss_yards = float(stats.get('defense_tackles_for_loss_yards') or 0)
                        data.defense_forced_fumbles = int(stats.get('defense_forced_fumbles') or 0)
                        data.defense_fumble_recoveries = int(stats.get('defense_fumble_recoveries') or 0)
                        data.defense_special_teams_fumble_recoveries = int(
                            stats.get('defense_special_teams_fumble_recoveries') or 0)
                        data.defense_miscellaneous_fumble_recoveries = int(
                            stats.get('defense_miscellaneous_fumble_recoveries') or 0)
                        data.defense_pass_defenses = int(stats.get('defense_pass_defenses') or 0)
                        data.penalty_yards = int(stats.get('penalty_yards') or 0)
                        data.total_touchdowns = int(stats.get('total_touchdowns') or 0)
                        sid = get_stats(c, player, data)
                        if sid is not None:
                            player.id = int(sid[0])
                        insert_stats_football(c, player, data)
                    if sport == 'hockey':
                        data = StatsHockey()
                        data.type = xstatgroup.contents[0].string
                        data.games_played = int(stats.get('games_played') or 0)
                        data.goals = int(stats.get('goals') or 0)
                        data.goals_period_1 = int(stats.get('goals_period_1') or 0)
                        data.goals_period_2 = int(stats.get('goals_period_2') or 0)
                        data.goals_period_3 = int(stats.get('goals_period_3') or 0)
                        data.goals_overtime = int(stats.get('goals_overtime') or 0)
                        data.goals_power_play = int(stats.get('goals_power_play') or 0)
                        data.goals_short_handed = int(stats.get('goals_short_handed') or 0)
                        data.game_winning_goals = int(stats.get('game_winning_goals') or 0)
                        data.assists = int(stats.get('assists') or 0)
                        data.plus_minus = int(stats.get('plus_minus') or 0)
                        data.penalty_minutes = int(stats.get('penalty_minutes') or 0)
                        data.shots = int(stats.get('shots') or 0)
                        data.faceoffs_won = int(stats.get('faceoffs_won') or 0)
                        data.faceoffs_lost = int(stats.get('faceoffs_lost') or 0)
                        data.time_on_ice_secs = int(stats.get('time_on_ice_secs') or 0)
                        data.time_on_ice_even_strength_secs = int(stats.get('time_on_ice_even_strength_secs') or 0)
                        data.time_on_ice_power_play_secs = int(stats.get('time_on_ice_power_play_secs') or 0)
                        data.time_on_ice_short_handed_secs = int(stats.get('time_on_ice_short_handed_secs') or 0)
                        data.shifts = int(stats.get('shifts') or 0)
                        sid = get_stats(c, player, data)
                        if sid is not None:
                            player.id = int(sid[0])
                        insert_stats_hockey(c, player, data)
                    if sport == 'soccer':
                        data = StatsSoccer()
                        data.type = xstatgroup.contents[0].string
                        data.goals = int(stats.get('goals') or 0)
                        data.goals_half_1 = int(stats.get('goals_half_1') or 0)
                        data.goals_half_2 = int(stats.get('goals_half_2') or 0)
                        data.goals_penalty = int(stats.get('goals_penalty') or 0)
                        data.goals_scored_first = int(stats.get('goals_scored_first') or 0)
                        data.own_goals = int(stats.get('own_goals') or 0)
                        data.yellow_cards = int(stats.get('yellow_cards') or 0)
                        data.red_cards = int(stats.get('red_cards') or 0)
                        data.discipline_points = int(stats.get('discipline_points') or 0)
                        sid = get_stats(c, player, data)
                        if sid is not None:
                            player.id = int(sid[0])
                        insert_stats_soccer(c, player, data)
        page.close()
conn.commit()
