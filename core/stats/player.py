from schema import replay
from db import models, session
from sqlalchemy import func, case, text, and_


class PlayerStats:
    def __init__(self, player_id=None, player_name=None) -> None:
        if player_id:
            self.player = session.query(models.Player).get(player_id)
        elif player_name:
            self.player = models.Player.from_name(player_name)
        else:
            raise ValueError("Requires player id or player name")
    
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
            wae = round((result.games_won - (result.expected_win_rate * result.games_played))/result.games_played, 3)*100   # round((wr-ewr)/wr, 3) if wr else 0
            result_dict = {
                'games_won': result.games_won,
                'games_played': result.games_played,
                'win_rate': wr,
                'expected_win_rate': ewr,
                'wae': wae
            }
        
            return result_dict
        
        return {}

    def head_2_head(self, player2_name: str):
        p1 = self.player
        p2 = models.Player.from_name(player2_name)
        '''
            player 1 wins | player 2 wins | total games | player 1 with player 2 | player 1 agaisnt player 2
        '''

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
            ).label('p2_win')
        ).group_by(
            t.replay_id
        ).filter(
            t.player_id.in_([p1.id, p2.id])
        ).having(
            text('in_match = 2')
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
            result.update({
                # 'p1': p1.display_name,
                # 'p2': p2.display_name,
                # 'games_played': len(matches),
                'match_rate %': round(together_games/all_games, 3)*100,
                # 'games_opposed': opposed_games,
                'win_together %': round(len([m for m in matches if m.p1_win == 1 and m.p2_win == 1])/together_games, 3)*100,
                # 'lost_together': len([m for m in matches if m.p1_win == 0 and m.p2_win == 0])/together_games,
                'p1_beats_p2 %': round(len([m for m in matches if m.p1_win == 1 and m.p2_win == 0])/opposed_games, 3)*100,
                #'p2_beat_p1': len([m for m in matches if m.p1_win == 0 and m.p2_win == 1])/opposed_games
            })
        
        return result

