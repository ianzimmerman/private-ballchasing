from statistics import mean
from typing import List

from core.skill import PrivateTrueSkill
from db import models, session
from schema import replay
from sqlalchemy import and_, case, func, text


class PlayerStats:
    def __init__(self, player_count: int=None, member_count: int=None) -> None:
        self.env = PrivateTrueSkill().env
        self.player_count = player_count
        self.member_count = member_count

        PrivateTrueSkill().rate_matches(player_count, member_count)

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
            models.Replay.player_count,
            models.PlayerResult.replay_id
        ).group_by(
            models.PlayerResult.player_id
        ).filter(
            models.PlayerResult.player_id==player.id,
            models.Replay.id == models.PlayerResult.replay_id
        )

        if self.player_count:
            q = q.filter(
                models.Replay.player_count==self.player_count
            )
        
        if self.member_count:
            q = q.filter(
                models.Replay.member_count>=self.member_count
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
                'wae': wae,
            })
        
            return results
        
        return None
    
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

        if self.player_count:
            q = q.filter(
                models.Replay.player_count==self.player_count
            )
        
        if self.member_count:
            q = q.filter(
                models.Replay.member_count>=self.member_count
            )

        matches = q.all()

        all_games = len(matches)
        together_games = len([m for m in matches if m.p1_win == m.p2_win])
        opposed_games = all_games - together_games

        result = {
            'p1': p1.display_name,
            'p2': p2.display_name,
            'trueskill_delta': round(self.env.expose(p1.rating) - self.env.expose(p2.rating),1),
            'games_played': all_games,
        }

        if all_games > 0:
            # win together rate
            wtr = round(len([m for m in matches if m.p1_win == 1 and m.p2_win == 1])/together_games, 3)*100 if together_games else 0
            
            # expected wins when together
            ewr = round(mean([m.expected_win_rate for m in matches if m.p1_win == m.p2_win]), 3)*100 if together_games else 0

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
                'p1_beats_p2 %': round(len([m for m in matches if m.p1_win == 1 and m.p2_win == 0])/opposed_games, 3)*100 if opposed_games else 0,
                #'p2_beat_p1': len([m for m in matches if m.p1_win == 0 and m.p2_win == 1])/opposed_games
            })
        
            return result
        
        return None

    def team_result(self, team_ids: List[str]):
        t = models.PlayerResult

        entities = [
            func.sum(
                case(
                    (and_(t.match_win==True, t.player_id==team_id), 1),
                    else_=0
                )
            ).label(f'{team_id}') for team_id in team_ids
        ]

        q = session.query(
            t.replay_id,
            func.count(
                case(
                    (t.player_id.in_(team_ids), 1),
                    else_=0
                )
            ).label('in_match'),
            *entities,
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
            t.player_id.in_(team_ids),
            models.Replay.id == models.PlayerResult.replay_id,
            models.Replay.player_count==len(team_ids)*2
        ).having(
            text(f'in_match = {len(team_ids)}')
        )
        
        if self.member_count:
            q = q.filter(
                models.Replay.member_count>=self.member_count
            )

        matches = q.all()
        wins = [m for m in matches if all([m[t_id]==1 for t_id in team_ids])]
        expected_wins = [w.expected_win_rate for w in wins]
        loses = [m for m in matches if all([m[t_id]==0 for t_id in team_ids])]

        if len(wins+loses) > 5:

            players = session.query(models.Player).filter(models.Player.id.in_(team_ids)).all()
            name_str = ', '.join([p.display_name for p in players])
            result =  {
                'team_name': name_str,
                'games_played': len(wins+loses),
                'win_rate': round(len(wins)/len(wins+loses), 3)*100,
                'exp_win_rate': round(mean(expected_wins),3)*100 if expected_wins else 0,
            }

            result.update({
                'delta': result['win_rate'] - result['exp_win_rate']
            })

            return result
        
        return None
