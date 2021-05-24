from db import models, session
from sqlalchemy import func, case


class PlayerStats:
    def __init__(self, player_id) -> None:
        self.player = session.query(models.Player).get(player_id)
    
    def win_rate(self, player_count=None):
        q = session.query(
            func.sum(
                case(
                    (models.PlayerResult.match_win==True, 1),
                    else_=0
                )
            ).label('games_won'),
            func.avg(
                case(
                    (models.PlayerResult.match_win==True, models.Replay.winner_chance),
                    else_=(1-models.Replay.winner_chance)
                )
            ).label('expected_win_rate'),
            func.count(models.PlayerResult.replay_id).label('games_played'),
            models.Replay.player_count
        ).group_by(
            models.PlayerResult.player_id
        ).filter(
            models.PlayerResult.player_id==self.player.id,
            models.Replay.id == models.PlayerResult.replay_id
        )

        if player_count:
            q = q.filter(
                models.Replay.player_count==player_count
            )

        result = q.first()
        if result:
            wr = round(result.games_won/result.games_played, 3)
            ewr = round(result.expected_win_rate, 3)
            wrae = round((wr-ewr)/wr, 3) if wr else 0
            result_dict = {
                'games_won': result.games_won,
                'games_played': result.games_played,
                'win_rate': wr,
                'expected_win_rate': ewr,
                'wrae': round(wrae*100, 1)
            }
        
            return result_dict
        
        return {}
    

    


