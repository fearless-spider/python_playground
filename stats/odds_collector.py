#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import traceback
import sys
from models.odds import Odds
from statsdb import db_open, db_close
from statsfiles import odds
from statsutils import path, debug, send_mail
from xmlutils import xml2obj

__author__ = 'bespider'

if __name__ == "__main__":
    try:
        cc = db_open()
        c = cc[0]
        conn = cc[1]

        for file in odds():
            if os.path.exists(path + file):
                if not debug:
                    print file

                # xml to obj
                sports_odds = xml2obj(open(path + file))
                for sport_game in sports_odds['sports-odds']['game']:
                    gamecode = sport_game.gamecode['global-id']
                    away_id = sport_game['visiting-team']['team-code']['id']
                    home_id = sport_game['home-team']['team-code']['id']
                    away_global_id = sport_game['visiting-team']['team-code']['global-id']
                    home_global_id = sport_game['home-team']['team-code']['global-id']
                    for game_line in sport_game['lines']['line']:
                        game_odds = Odds(c)
                        game_odds.gamecode = gamecode
                        game_odds.scope = game_line.scope.name
                        # opening line
                        game_odds.line = 'opening'
                        game_odds.fav_id = game_line['opening-line']['fav-id']
                        if game_odds.fav_id == away_id:
                            game_odds.fav_id = away_global_id
                        else:
                            game_odds.fav_id = home_global_id
                        game_odds.pts = game_line['opening-line']['fav-pts']
                        game_odds.fav = game_line['opening-line']['fav-money']
                        game_odds.underdog = game_line['opening-line']['underdog-money']
                        game_odds.home = game_line['opening-line']['home-money']
                        game_odds.away = game_line['opening-line']['away-money']
                        game_odds.total = game_line['opening-line']['total']
                        game_odds.over = game_line['opening-line']['over-money']
                        game_odds.under = game_line['opening-line']['under-money']
                        game_odds.save()

                        game_odds = Odds(c)
                        game_odds.gamecode = gamecode
                        game_odds.scope = game_line.scope.name
                        # current line
                        game_odds.line = 'current'
                        game_odds.fav_id = game_line['current-line']['fav-id']
                        if game_odds.fav_id == away_id:
                            game_odds.fav_id = away_global_id
                        else:
                            game_odds.fav_id = home_global_id
                        game_odds.pts = game_line['current-line']['fav-pts']
                        game_odds.fav = game_line['current-line']['fav-money']
                        game_odds.underdog = game_line['current-line']['underdog-money']
                        game_odds.home = game_line['current-line']['home-money']
                        game_odds.away = game_line['current-line']['away-money']
                        game_odds.total = game_line['current-line']['total']
                        game_odds.over = game_line['current-line']['over-money']
                        game_odds.under = game_line['current-line']['under-money']
                        game_odds.save()

        db_close(c, conn)
    except:
        if debug:
            print traceback.format_exc()
        else:
            send_mail("odds", traceback.format_exc())
        sys.exit(1)
