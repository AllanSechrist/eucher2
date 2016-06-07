from objects import player

class EucPlayer(player.Player):
    """
    adds attributes to player class unique to Eucher
    """

    def __init__(self, player_number):
        super().__init__(player_number)

        self.took_last_trick = False
        self.tricks = 0