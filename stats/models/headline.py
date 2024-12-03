import ftplib
import os
import traceback
from statsutils import slugfy, debug, replace_nonascii

__author__ = 'fearless'


class Image():
    def __init__(self, c=None):
        self.story_id = ''
        self.image_id = ''
        self.source = ''
        self.caption = ''
        self.c = c

    def __repr__(self):
        return "<Image %s>" % (self.image_id)

    def save(self):
        print "save image for story " + self.story_id
        sql = """INSERT INTO wp_bp_story_images (
                    `story_id`,
                    `source`,
                    `caption`,
                    `image_id`
        ) VALUES (
            '%s',
            '%s',
            '%s',
            '%s'
        )
        ;""" % (
            self.story_id,
            replace_nonascii(self.source),
            replace_nonascii(self.caption),
            self.image_id
        )
        # print sql
        self.c.execute(sql)


class Headline():
    def __init__(self):
        self.id = 0
        self.story_id = ''
        self.original_id = ''
        self.filename = ''
        self.headline = ''
        self.version = 0
        self.images = []
        self.code = ''

    def __repr__(self):
        return "<Headline %s>" % (self.story_id)

    def upload(self):
        print "upload images for story " + self.story_id
        if not debug:
            s = ftplib.FTP()
            s.set_pasv(0)
            success = s.connect('')

            s.login('', '')
            yyyy = self.story_id[:4]
            mm = self.story_id[4:6]
            dd = self.story_id[6:8]
            story_dir = yyyy + '/' + mm + '/' + dd
            # print story_dir
            # create dir YYYYMMDD
            try:
                s.mkd('/var/www/html/wp-content/uploads/images/' + yyyy)
            except:
                pass

            try:
                s.mkd('/var/www/html/wp-content/uploads/images/' + yyyy + '/' + mm)
            except:
                pass

            try:
                s.mkd('/var/www/html/wp-content/uploads/images/' + yyyy + '/' + mm + '/' + dd)
            except:
                pass

            for image in self.images:
                try:
                    #  Test to see if the file exists by getting the file size by name.
                    #  If a -1 is returned, the file does not exist.
                    fileSize = s.size(
                        "/var/www/html/wp-content/uploads/images/" + story_dir + "/" + image.image_id + "-p2.jpeg")
                    b = os.path.getsize('/home/sstreet_feed/' + image.image_id + '-p2.jpeg')
                    if fileSize != b:
                        s.delete(
                            '/var/www/html/wp-content/uploads/images/' + story_dir + "/" + image.image_id + '-p2.jpeg')
                        f = open('/home/sstreet_feed/' + image.image_id + '-p2.jpeg', 'rb')
                        s.storbinary(
                            'STOR /var/www/html/wp-content/uploads/images/' + story_dir + "/" + image.image_id + '-p2.jpeg',
                            f)
                        f.close()
                    else:
                        f = open('/home/sstreet_feed/' + image.image_id + '-p2.jpeg', 'rb')
                        s.storbinary(
                            'STOR /var/www/html/wp-content/uploads/images/' + story_dir + "/" + image.image_id + '-p2.jpeg',
                            f)
                        f.close()
                    image.save()
                except:
                    try:
                        f = open('/home/sstreet_feed/' + image.image_id + '-p2.jpeg', 'rb')
                        s.storbinary(
                            'STOR /var/www/html/wp-content/uploads/images/' + story_dir + "/" + image.image_id + '-p2.jpeg',
                            f)
                        f.close()
                        image.save()
                    except:
                        print traceback.format_exc()
                        pass


class Story(Headline):
    def __init__(self, publishedAt=None, content=None, byLine=None, byTitle=None, c=None):
        Headline.__init__(self)
        self.published_at = ''
        self.content = ''
        self.byline = ''
        self.bytitle = ''
        self.teams = []
        self.c = c

    def __repr__(self):
        return "<Story %s>" % (self.story_id)

    def save(self):
        self.upload()
        print "save story" + self.story_id
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
        ) VALUES (
            %d,
            '%s',
            '%s',
            '%s',
            '%s',
            '%d',
            '%s',
            '%s',
            '%s',
            '%s'
        )
        ON DUPLICATE KEY UPDATE
        `published_at` = VALUES(`published_at`),
        `headline` = VALUES(`headline`),
        `content` = VALUES(`content`),
        `version` = VALUES(`version`),
        `byline` = VALUES(`byline`),
        `bytitle` = VALUES(`bytitle`)
        ;""" % (
            self.id,
            self.published_at,
            self.story_id,
            self.code,
            slugfy(self.headline, "-"),
            int(self.version),
            replace_nonascii(self.headline),
            replace_nonascii(self.content),
            replace_nonascii(self.byline),
            replace_nonascii(self.bytitle)
        )
        self.c.execute(sql)

        for team in set(self.teams):
            # print "save team story" + team
            sql = """INSERT INTO wp_bp_story_teams (
                    `story_id`,
                    `team_global_id`
            ) VALUES (
                '%s',
                '%s'
            )
            ;""" % (
                self.story_id,
                team
            )
            # print sql
            self.c.execute(sql)
