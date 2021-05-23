from schema.replay import Player, Replay


class Match:
    def __init__(self, replay: Replay) -> None:
        self.replay = replay
        self.blue_score = self.replay.blue.goals or 0
        self.orange_score = self.replay.orange.goals or 0

    @property
    def winners(self):
        if self.blue_score > self.orange_score:
            return self.replay.blue.players
        else:
            return self.replay.orange.players
    
    @property
    def losers(self):
        if self.blue_score < self.orange_score:
            return self.replay.blue.players
        else:
            return self.replay.orange.players
    
    @property
    def players(self):
        return self.winners + self.losers
    
    def player_won(self, player: Player):
        return player in self.winners
    