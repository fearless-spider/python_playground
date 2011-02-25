# -*- coding: utf-8 -*-
import os
import re
import glob
from statsutils import now_finals, date_format_mlb, date_format, debug, now, path

__author__ = 'fearless'

finalstats_files = (
    # filename.xml,league,league_id
    ('NBA_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'nba', 2, '2'),
    ('CFB_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'ncaaf', 10, '130'),
    ('CBK_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'ncaab', 8, '128'),
    ('WCBK_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'wncaab', 9, '129'),
    ('NHL_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'nhl', 4, '4'),
    ('NFL_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'nfl', 3, '3'),
    ('EPL_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'epl', 19, '4883'),
    ('SERI_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'seri', 20, '4882'),
    ('BUND_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'bund', 14, '4881'),
    ('LIGA_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'liga', 16, '4886'),
    ('MLS_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'mls', 11, '262'),
    ('FMF_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'fmf', 17, '4885'),
    ('FRAN_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'fran', 18, '4884'),
    ('CHLG_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'chlg', 15, '4887'),
    ('WNBA_FINALBOX?' + now_finals.strftime(date_format) + '*.XML', 'wnba', 21, '5082'),
    ('MLB_FINALBOX?32' + now_finals.strftime(date_format_mlb) + '*.XML', 'mlb', 5, '5')
)

teaminfo_files = (
    # group_id,sport_id,filename.xml,league
    (4881, 6, 'BUND_TEAM_INFO.XML', 'bund'),
    (4882, 6, 'SERI_TEAM_INFO.XML', 'seri'),
    (4883, 6, 'EPL_TEAM_INFO.XML', 'epl'),
    (4884, 6, 'FRAN_TEAM_INFO.XML', 'fran'),
    (4885, 6, 'FMF_TEAM_INFO.XML', 'fmf'),
    (4886, 6, 'LIGA_TEAM_INFO.XML', 'liga'),
    (4887, 6, 'CHLG_TEAM_INFO.XML', 'chlg'),
    (262, 6, 'MLS_TEAM_INFO.XML', 'mls'),
    (2, 1, 'NBA_TEAM_INFO.XML', 'nba'),
    (5082, 1, 'WNBA_TEAM_INFO.XML', 'wnba'),
    (129, 1, 'WCBK_TEAM_INFO.XML', 'wncaab'),
    (128, 1, 'CBK_TEAM_INFO.XML', 'ncaab'),
    (130, 3, 'CFB_TEAM_INFO.XML', 'ncaaf'),
    (5, 2, 'MLB_TEAM_INFO.XML', 'mlb'),
    (3, 3, 'NFL_TEAM_INFO.XML', 'nfl'),
    (4, 4, 'NHL_TEAM_INFO.XML', 'nhl')
)

allroster_files = (
    # filename.xml,league
    ('NBA_ALL_ROSTER.XML', '2'),
    ('WNBA_ALL_ROSTER.XML', '5082'),
    ('CFB_ROSTER.XML', '130'),
    ('CBK_ROSTER.XML', '128'),
    ('WCBK_ROSTER.XML', '129'),
    ('NHL_ALL_ROSTER.XML', '4'),
    ('MLB_ALLROSTER.XML', '5'),
    ('NFL_ALL_ROSTER.XML', '3'),
    ('MLS_ROSTER.XML', '262'),
    ('FRAN_ROSTER.XML', '4884'),
    ('BUND_ROSTER.XML', '4881'),
    ('SERI_ROSTER.XML', '4882'),
    ('CHLG_ROSTER.XML', '4887'),
    ('EPL_ROSTER.XML', '4883'),
    ('FMF_ROSTER.XML', '4885'),
    ('LIGA_ROSTER.XML', '4886')
)


def stories():
    files = os.listdir(path)
    stories = []
    for file in files:
        if debug:
            if re.match(r'\S+_STORY\S+', file) is not None:
                stories.append(file)
        else:
            if re.match(r'\S+_STORY\S+' + now.strftime("%Y%m%d"), file) is not None:
                stories.append(file)
    return stories


def headlines():
    files = os.listdir(path)
    headlines = []
    for file in files:
        if re.match(r'\S+_HEADLINES\S+', file) is not None:
            headlines.append(file)
    return headlines


def odds():
    files = os.listdir(path)
    odds_files = []
    for file in files:
        if re.match(r'\S+_ODDS\S+', file) is not None:
            odds_files.append(file)
    return odds_files


stories_code = (
    (2025, 'GOLF'),
    (2026, 'TENNIS'),
    (4881, 'IFB'),
    (262, 'MLS'),
    (2, 'NBA'),
    (5082, 'WNBA'),
    (129, 'WCBK'),
    (128, 'CBK'),
    (130, 'CFB'),
    (5, 'MLB'),
    (3, 'NFL'),
    (4, 'NHL')
)

stories_code_dict = {
    'GOLF': 2025,
    'TENNIS': 2026,
    'IFB': 4881,
    'MLS': 262,
    'NBA': 2,
    'WNBA': 5082,
    'WCBK': 129,
    'CBK': 128,
    'CFB': 130,
    'MLB': 5,
    'NFL': 3,
    'NHL': 4
}

schedule_files = (
    # group_id,filename.xml,league
    (2, 'NBA_SCHEDULE.XML', 'nba'),
    (5082, 'WNBA_SCHEDULE.XML', 'wnba'),
    (128, 'CBK_SCHEDULE.XML', 'ncaab'),
    (129, 'WCBK_SCHEDULE.XML', 'wncaab'),
    (4, 'NHL_SCHEDULE.XML', 'nhl'),
    (3, 'NFL_SCHEDULE.XML', 'nfl'),
    (130, 'CFB_SCHEDULE_ALL.XML', 'ncaaf'),
    (262, 'MLS_SCHEDULE.XML', 'mls'),
    (4881, 'BUND_SCHEDULE.XML', 'bund'),
    (4887, 'CHLG_SCHEDULE.XML', 'chlg'),
    (4886, 'LIGA_SCHEDULE.XML', 'liga'),
    (4885, 'FMF_SCHEDULE.XML', 'fmf'),
    (4884, 'FRAN_SCHEDULE.XML', 'fran'),
    (4883, 'EPL_SCHEDULE.XML', 'epl'),
    (4882, 'SERI_SCHEDULE.XML', 'seri'),
    (5, 'MLB_SCHEDULE.XML', 'mlb'),
)

playerstats_files = glob.glob(path + '/*_PLAYER_STATS*.XML')

live_files = (
    # league_id, filename.xml,league
    (10, 'CFB_LIVE.XML', '130'),
    (3, 'NFL_LIVE.XML', '3'),
    (2, 'NBA_LIVE.XML', '2'),
    (21, 'WNBA_SCORES.XML', '5082'),
    (8, 'CBK_LIVE.XML', '128'),
    (9, 'WCBK_SCORES.XML', '129'),
    (4, 'NHL_LIVE.XML', '4'),
    (14, 'BUND_LIVE.XML', '4881'),
    (17, 'FMF_LIVE.XML', '4885'),
    (18, 'FRAN_LIVE.XML', '4884'),
    (20, 'SERI_LIVE.XML', '4882'),
    (15, 'CHLG_LIVE.XML', '4887'),
    (16, 'LIGA_LIVE.XML', '4886'),
    (19, 'EPL_LIVE.XML', '4883'),
    (11, 'MLS_LIVE.XML', '262'),
    (5, 'MLB_LIVE.XML', '5'),
)

leaders_files = (
    # league, filename.xml
    ('NBA', 'NBA_LEADERS.XML'),
    ('WNBA', 'WNBA_LEADERS.XML'),
    ('NFL', 'NFL_LEADERS.XML'),
    ('NCAA FB', 'CFB_LEADERS.XML'),
    ('NCAA BB', 'CBK_LEADERS.XML'),
    ('WNCAAB', 'WCBK_LEADERS.XML'),
    ('NHL', 'NHL_LEADERS.XML'),
    ('EPL', 'EPL_LEADERS.XML'),
    ('CHLG', 'CHLG_LEADERS.XML'),
    ('SERI', 'SERI_LEADERS.XML'),
    ('BUND', 'BUND_LEADERS.XML'),
    ('FMF', 'FMF_LEADERS.XML'),
    ('FRAN', 'FRAN_LEADERS.XML'),
    ('LIGA', 'LIGA_LEADERS.XML'),
    ('MLS', 'MLS_LEADERS.XML'),
    ('MLB', 'MLB_LEADERS$2012.XML'),
)
