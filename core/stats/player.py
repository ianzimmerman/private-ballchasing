from schema import replay
from db import models, session
from sqlalchemy import func, case, text, and_
from statistics import mean
from core.skill import PrivateTrueSkill



class PlayerStats:
    def __init__(self, lobby_size: int=None) -> None:
        self.env = PrivateTrueSkill().env
        self.lobby_size = lobby_size
    
    def win_rate(self, player: models.Player):
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
            models.PlayerResult.player_id==player.id,
            models.Replay.id == models.PlayerResult.replay_id
        )

        if self.lobby_size:
            q = q.filter(
                models.Replay.player_count==self.lobby_size
            )

        stats = q.first()

        results = {
            'display_name': player.display_name,
            'trueskill': round(self.env.expose(player.rating),1)
        }

        if stats:
            wr = round(stats.games_won/stats.games_played, 3)
            ewr = round(stats.expected_win_rate, 3)
            wae = round((stats.games_won - (stats.expected_win_rate * stats.games_played))/stats.games_played, 3)*100   # round((wr-ewr)/wr, 3) if wr else 0
            results.update({
                'games_won': stats.games_won,
                'games_played': stats.games_played,
                'win_rate': wr,
                'expected_win_rate': ewr,
                'wae': wae
            })
        
        return results
    
    def head_2_head(self, player1: models.Player, player2: models.Player):
        p1 = player1
        p2 = player2

        t = models.PlayerResult

        q = session.query(
            t.replay_id,
            func.count(
                case(
                    (t.player_id.in_([p1.id, p2.id]), 1),
                    else_=0
                )
            ).label('in_match'),
            func.sum(
                case(
                    (and_(t.match_win==True, t.player_id==p1.id), 1),
                    else_=0
                )
            ).label('p1_win'),
            func.sum(
                case(
                    (and_(t.match_win==True, t.player_id==p2.id), 1),
                    else_=0
                )
            ).label('p2_win'),
            func.avg(
                case(
                    (t.match_win==True, models.Replay.winner_chance),
                    else_=(1-models.Replay.winner_chance)
                )
            ).label('expected_win_rate'),
            models.Replay.player_count
        ).group_by(
            t.replay_id
        ).filter(
            t.player_id.in_([p1.id, p2.id]),
            models.Replay.id == models.PlayerResult.replay_id
        ).having(
            text('in_match = 2')
        )

        if self.lobby_size:
            q = q.filter(
                models.Replay.player_count==self.lobby_size
            )

        matches = q.all()

        all_games = len(matches)
        together_games = len([m for m in matches if m.p1_win == m.p2_win])
        opposed_games = all_games - together_games

        result = {
            'p1': p1.display_name,
            'p2': p2.display_name,
            'games_played': all_games,
        }

        if all_games > 0:
            # win together rate
            wtr = round(len([m for m in matches if m.p1_win == 1 and m.p2_win == 1])/together_games, 3)*100
            
            # expected wins when together
            ewr = round(mean([m.expected_win_rate for m in matches if m.p1_win == m.p2_win]), 3)*100

            result.update({
                # 'p1': p1.display_name,
                # 'p2': p2.display_name,
                # 'games_played': len(matches),
                'match_rate %': round(together_games/all_games, 3)*100,
                # 'games_opposed': opposed_games,
                'win_together %': wtr,
                'expected_win %': ewr,
                '+/-': wtr - ewr,
                # 'lost_together': len([m for m in matches if m.p1_win == 0 and m.p2_win == 0])/together_games,
                'p1_beats_p2 %': round(len([m for m in matches if m.p1_win == 1 and m.p2_win == 0])/opposed_games, 3)*100,
                #'p2_beat_p1': len([m for m in matches if m.p1_win == 0 and m.p2_win == 1])/opposed_games
            })
        
        return result
