#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from statsfiles import stories, stories_code
from statsutils import replace_nonascii, find_value_in_array2args, slugfy, path, debug, send_mail
from statsdb import db_open, db_close, get_stories, get_teams_with_players, insert_stories, insert_images, \
    insert_teams_story

print debug

if not debug:
    import ftplib

__author__ = 'fearless'


class NBAHandler(ContentHandler):
    def __init__(self):
        self.id = 0
        self.date = ''
        self.time = ''
        self.story_id = ''
        self.code = ''
        self.slug = ''
        self.version = ''
        self.headline = ''
        self.teamswithplayers = []
        self.teams = []
        self.content = ''
        self.byline = ''
        self.bytitle = ''
        self.image_id = ''
        self.source = ''
        self.caption = ''
        self.insertdata = []
        self.insertimages = []
        self.Insert = True

    def startElement(self, name, attrs):
        if name == 'date':
            self.date = attrs.get('year') + '-' + attrs.get('month') + '-' + attrs.get('date')
        elif name == 'time':
            self.time = attrs.get('hour') + ':' + attrs.get('minute') + ':' + attrs.get('second')
        elif name == 'story':
            self.code = attrs.get('code')
            for code in stories_code:
                if self.code == code[1]:
                    self.code = str(code[0])
            self.story_id = attrs.get('id')
            self.slug = replace_nonascii(attrs.get('slug'))
            self.version = attrs.get('version')
            self.stories = get_stories(c, self.code)
            self.teamswithplayers = get_teams_with_players(c)
            self.insertdata = []
        elif name == 'header':
            self.headline = replace_nonascii(attrs.get('headline'))
            self.byline = replace_nonascii(attrs.get('byline'))
            self.bytitle = attrs.get('bytitle')
            self.bytitle = replace_nonascii(attrs.get('bytitle'))
        elif name == 'team-code':
            self.teams.append(attrs.get('global-id'))
        elif name == 'player-code':
            player_global_id = attrs.get('global-id')
            team_global_id = find_value_in_array2args(self.teamswithplayers, player_global_id)
            if team_global_id:
                if team_global_id not in self.teams:
                    self.teams.append(team_global_id)
        elif name == 'image':
            self.image_id = attrs.get('id')
            self.source = replace_nonascii(attrs.get('source'))
            self.caption = replace_nonascii(attrs.get('caption'))
            # print self.caption
        elif name == 'p':
            self.content = self.content + replace_nonascii("<p>" + attrs.get('text') + "</p>")
        return

    def endElement(self, name):
        if name == 'story':
            if find_value_in_array2args(self.stories, self.story_id) is not None:
                self.Insert = False
        elif name == 'news-story' and self.Insert:
            data = str.join(',', self.insertdata)
            insert_stories(c, data)
            data = str.join(',', self.insertimages)
            insert_images(c, data)
            insertteams = []
            for team in self.teams:
                insertteams.append("('" + self.story_id + "','" + team + "')")
            data = str.join(',', insertteams)
            insert_teams_story(c, data)
        elif name == 'image' and self.Insert:
            self.insertimages.append("("
                                     + str(0) +
                                     ",'"
                                     + self.story_id +
                                     "','"
                                     + self.source +
                                     "','"
                                     + self.caption +
                                     "','"
                                     + self.image_id +
                                     "')")
            if not debug:
                yyyy = self.story_id[:4]
                mm = self.story_id[4:6]
                dd = self.story_id[6:8]
                story_dir = yyyy + '/' + mm + '/' + dd
                print story_dir
                # create dir YYYYMMDD
                try:
                    s.mkd('/var/www/html/wp-content/uploads/images/' + yyyy)
                    # print yyyy
                except:
                    # print traceback.format_exc()
                    pass

                try:
                    s.mkd('/var/www/html/wp-content/uploads/images/' + yyyy + '/' + mm)
                    # print mm
                except:
                    # print traceback.format_exc()
                    pass

                try:
                    s.mkd('/var/www/html/wp-content/uploads/images/' + yyyy + '/' + mm + '/' + dd)
                    # print dd
                except:
                    # print traceback.format_exc()
                    pass

                try:
                    #  Test to see if the file exists by getting the file size by name.
                    #  If a -1 is returned, the file does not exist.
                    fileSize = s.size(
                        "/var/www/html/wp-content/uploads/images/" + story_dir + "/" + self.image_id + "-p2.jpeg")
                    b = os.path.getsize('/home/sstreet_feed/' + self.image_id + '-p2.jpeg')
                    if fileSize != b:
                        s.delete(
                            '/var/www/html/wp-content/uploads/images/' + story_dir + "/" + self.image_id + '-p2.jpeg')
                        f = open('/home/sstreet_feed/' + self.image_id + '-p2.jpeg', 'rb')
                        s.storbinary(
                            'STOR /var/www/html/wp-content/uploads/images/' + story_dir + "/" + self.image_id + '-p2.jpeg',
                            f)
                        f.close()
                except:
                    f = open('/home/sstreet_feed/' + self.image_id + '-p2.jpeg', 'rb')
                    s.storbinary(
                        'STOR /var/www/html/wp-content/uploads/images/' + story_dir + "/" + self.image_id + '-p2.jpeg',
                        f)
                    f.close()

            self.source = ''
            self.caption = ''
            self.image_id = ''

        elif name == 'content' and self.Insert:
            self.insertdata.append("("
                                   + str(0) +
                                   ",'"
                                   + self.date + ' ' + self.time +
                                   "','"
                                   + self.story_id +
                                   "','"
                                   + self.code +
                                   "','"
                                   + slugfy(self.slug, "-") +
                                   "','"
                                   + self.version +
                                   "','"
                                   + self.headline +
                                   "','"
                                   + self.content +
                                   "','"
                                   + self.byline +
                                   "','"
                                   + self.bytitle +
                                   "')")


if __name__ == "__main__":
    if os.access(os.path.expanduser("~/.lockfile.stories.lock"), os.F_OK):
        # if the lockfile is already there then check the PID number
        # in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.stories.lock"), "r")
        pidfile.seek(0)
        old_pid = pidfile.readline()
        # Now we check the PID from lock file matches to the current
        # process PID
        if os.path.exists("/proc/%s" % old_pid):
            print "You already have an instance of the program running"
            print "It is running as process %s," % old_pid
            sys.exit(1)
        else:
            print "File is there but the program is not running"
            print "Removing lock file for the: %s as it can be there                 because of the program last time it was run" % old_pid
            os.remove(os.path.expanduser("~/.lockfile.stories.lock"))
    else:
        pidfile = open(os.path.expanduser("~/.lockfile.stories.lock"), "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close()

        try:
            if not debug:
                s = ftplib.FTP()
                s.set_pasv(0)
                success = s.connect('')

                s.login('', '')

            cc = db_open()
            c = cc[0]
            conn = cc[1]
            parser = make_parser()
            for story in stories():
                if debug:
                    print story
                curHandler = NBAHandler()
                parser.setContentHandler(curHandler)
                parser.parse(open(path + story))

            db_close(c, conn)
            if not debug:
                s.quit()

            os.remove(os.path.expanduser("~/.lockfile.stories.lock"))
        except:
            os.remove(os.path.expanduser("~/.lockfile.stories.lock"))
            if debug:
                print traceback.format_exc()
            else:
                send_mail("stories", traceback.format_exc())
            sys.exit(1)
