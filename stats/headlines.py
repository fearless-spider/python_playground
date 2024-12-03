#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from models.headline import Image, Story
from statsfiles import stories_code_dict, headlines
from statsutils import find_value_in_array2args, path, debug, send_mail
from statsdb import db_open, db_close, get_stories, get_teams_with_players
from xmlutils import xml2obj

if not debug:
    import ftplib

__author__ = 'fearless'

if __name__ == "__main__":
    try:
        cc = db_open()
        c = cc[0]
        conn = cc[1]

        for file in headlines():
            if os.path.exists(path + file):
                if not debug:
                    print file

                teamswithplayers = get_teams_with_players(c)
                # xml to obj
                sportnews = xml2obj(open(path + file))
                for news_story in sportnews['sports-news-stories']['news-stories']:
                    for stories in news_story['news-story']:
                        for story in stories['story']:
                            # <story type="headline" id="1" code="NBA" >
                            code = stories_code_dict[story.code]
                            stories_in = get_stories(c, code)
                            for headlines in story['headlines']:
                                headLine = Story(c=c)
                                headLine.story_id = headlines['headline'].id
                                headLine.original_id = headlines['headline'].original_id
                                headLine.id = find_value_in_array2args(stories_in, headLine.story_id)
                                if headLine.id is None:
                                    headLine.id = find_value_in_array2args(stories_in, headLine.original_id)
                                    if headLine.id is None:
                                        headLine.id = 0

                                headLine.filename = headlines['headline'].name
                                if not os.path.exists(path + headLine.filename):
                                    continue
                                headLine.headline = headlines['headline'].text
                                headLine.version = headlines['headline'].version
                                headLine.code = code
                                if headlines['image']:
                                    headLine.images = []
                                    for img in headlines['image']:
                                        image = Image(c=c)
                                        image.story_id = headLine.story_id
                                        image.image_id = img.id
                                        image.source = img.source
                                        if not image.source:
                                            image.source = ""
                                        image.caption = img.caption
                                        if not image.caption:
                                            image.caption = ""
                                        headLine.images.append(image)
                                if os.path.exists(path + headLine.filename):
                                    head_story = xml2obj(open(path + headLine.filename))
                                    # <sports-news-stories>
                                    for sport_news_stories in head_story['sports-news-stories']:
                                        headLine.published_at = sport_news_stories.date.year + '-' + sport_news_stories.date.month + '-' + sport_news_stories.date.date
                                        headLine.published_at += ' ' + sport_news_stories.time.hour + ':' + sport_news_stories.time.minute + ':' + sport_news_stories.time.second
                                        for news_stories in sport_news_stories['news-stories']['news-story']['story']:
                                            headLine.byline = news_stories.header.byline
                                            headLine.bytitle = news_stories.header.bytitle
                                            headLine.content = ''
                                            for content in news_stories.content['p']:
                                                headLine.content += '<p>' + content.text + '</p>'
                                            if news_stories.team:
                                                for team in news_stories.team:
                                                    headLine.teams.append(team['team-code']['global-id'])
                                            if news_stories.players:
                                                for player in news_stories.players.player:
                                                    player_id = player['player-code']['global-id']
                                                    team_id = find_value_in_array2args(teamswithplayers, player_id)
                                                    if team_id:
                                                        headLine.teams.append(team_id)
                                    headLine.save()

        db_close(c, conn)
    except:
        if debug:
            print traceback.format_exc()
        else:
            send_mail("headlines", traceback.format_exc())
        sys.exit(1)
