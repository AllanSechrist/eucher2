

class Player(object):
    """
    creates player object
    """

    List = []

    def __init__(self, player_number):
        self.hand = None
        self.player_number = player_number
        Player.List.append(self)


class Team(object):
    """
    creates team object
    """

    List = []

    def __init__(self, team_number):
        self.points = 0
        self.team_number = team_number
        Team.List.append(self)

