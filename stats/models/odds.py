__author__ = 'bespider'


class Odds():
    def __init__(self, c=None):
        self.id = 0
        self.gamecode = ''
        self.fav_id = ''
        self.scope = ''
        self.line = ''
        self.pts = ''
        self.fav = ''
        self.underdog = ''
        self.home = ''
        self.away = ''
        self.total = ''
        self.over = ''
        self.under = ''
        self.c = c

    def __repr__(self):
        return "<Odds %s>" % (self.gamecode)

    def save(self):
        self.id = self.get()
        print "save odds for game " + self.gamecode
        sql = """INSERT INTO wp_bp_odds (
                    `id`,
                    `gamecode`,
                    `fav_id`,
                    `scope`,
                    `line`,
                    `pts`,
                    `fav`,
                    `underdog`,
                    `home`,
                    `away`,
                    `total`,
                    `over`,
                    `under`
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
            '%s'
        )
        ON DUPLICATE KEY UPDATE
        `fav_id` = VALUES(`fav_id`),
        `scope` = VALUES(`scope`),
        `line` = VALUES(`line`),
        `pts` = VALUES(`pts`),
        `fav` = VALUES(`fav`),
        `underdog` = VALUES(`underdog`),
        `home` = VALUES(`home`),
        `away` = VALUES(`away`),
        `total` = VALUES(`total`),
        `over` = VALUES(`over`),
        `under` = VALUES(`under`)
        ;""" % (
            self.id,
            self.gamecode,
            self.fav_id,
            self.scope,
            self.line,
            self.pts,
            self.fav,
            self.underdog,
            self.home,
            self.away,
            self.total,
            self.over,
            self.under
        )
        #        print sql
        self.c.execute(sql)

    def get(self):
        print "get one odds"
        sql = "SELECT id FROM wp_bp_odds WHERE gamecode = '%s' AND scope = '%s' AND line = '%s'" % (
        self.gamecode, self.scope, self.line)
        self.c.execute(sql)
        result = self.c.fetchone()
        if result:
            return result[0]
        else:
            return 0
