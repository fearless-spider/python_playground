__author__ = 'fearless'


class Team():
    def __init__(self, id, group_id, global_id, city, name, alias, season, conference, division, league_id):
        self.id = id
        self.group_id = group_id
        self.global_id = global_id
        self.city = city
        self.name = name
        self.alias = alias
        self.season = season
        self.conference = conference
        self.division = division
        self.league_id = league_id

    def __repr__(self):
        return "<Team %s>" % (self.name)


class Group():
    def __init__(self, id, global_id, city, name, alias, parent_id, sport, state, country):
        self.id = id
        self.global_id = global_id
        self.city = city
        self.name = name
        self.alias = alias
        self.parent_id = parent_id
        self.sport = sport
        self.state = state
        self.country = country

    def __repr__(self):
        return "<Team %s>" % (self.name)
