from schema.replay import Player, Replay
from config import MEMBER_IDS
import hashlib

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
        all_players = self.winners + self.losers
        return [p for p in all_players if self.play_percentage(p) >= .5]
    
    def play_percentage(self, player: Player):
        p_duration = player.end_time - player.start_time
        return p_duration/self.replay.duration
    
    def player_won(self, player: Player):
        return player in self.winners

    @property
    def group_member_count(self):
        members_in_match = []
        for player in self.players:
            str_id = f"{player.id.platform}:{player.id.id}"
            if str_id in MEMBER_IDS:
                members_in_match.append(str_id)
        
        return len(members_in_match)

    
    @property
    def match_hash(self):
        match_date = self.replay.date.strftime("%Y%m%d")
        blue_points = sum([p.score for p in self.replay.blue.players])
        orange_points = sum([p.score for p in self.replay.orange.players])
        
        hash_data = f"{match_date}-{blue_points}-{orange_points}".encode()
        return hashlib.sha224(hash_data).hexdigest()
    