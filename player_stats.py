import argparse
from typing import List

import trueskill
from tabulate import tabulate

from config import MEMBER_IDS
from core.stats.player import PlayerStats
from db import models, session

ENV = trueskill.TrueSkill(draw_probability=0)
parser = argparse.ArgumentParser(description='Find some stats')
parser.add_argument('stat', metavar='S', type=str, help='rating, headsup')
parser.add_argument('--n', type=int, help='limit to lobbies with n players')
parser.add_argument('--min', type=int, help='limit to min x games played')
parser.add_argument('--p1', type=str, help='player 1')
parser.add_argument('--p2', type=str, help='player 2')

def stat_print(stats: List[dict], sort_key: str=None):
    if sort_key:
        stats = sorted(stats, key=lambda x: x.get(sort_key), reverse=True)
    print(tabulate(stats, headers="keys", tablefmt="pipe"))

if __name__ == "__main__":
    args = parser.parse_args()
    print(' ')
    print(args)
    print(' ')

    if args.stat == 'rating':
        q = session.query(models.Player)
        players = sorted(q.all(), key=ENV.expose, reverse=True)
        leaders = []
        for p in players:
            stats = PlayerStats(args.n).win_rate(p)
            if stats.get('games_played', 0) >= (args.min or 25):
                leaders.append(stats)
        

        stat_print(leaders)
        
    elif args.stat == 'headsup':
        if not args.p1:
            raise ValueError('needs --p1=nick')
        
        stats = PlayerStats(args.n)
        player1 = models.Player.from_name(args.p1)
        player2 = models.Player.from_name(args.p2) if args.p2 else None
        
        headsup = []
        if player1 and player2:
            print(player1.aka)
            print(player2.aka)
            headsup.append(
                stats.head_2_head(player1, player2)
            )

            p1_wins = stats.win_rate(player1)
            p2_wins = stats.win_rate(player2)
            divider = {}
            deltas = {}
            for k, v in p1_wins.items():
                if not isinstance(v, str):
                    deltas[k] = p1_wins[k] - p2_wins[k]
                else:
                    deltas[k] = " "

            stat_print([p1_wins, p2_wins, divider, deltas])
            print(" ")

        elif player1:
            for player2 in session.query(models.Player):
                # player2 = session.query(models.Player).get(player_id)
                if player1 != player2:
                    headsup.append(
                        stats.head_2_head(player1, player2)
                    )
            
        
        stat_print(headsup, 'games_played')
    
    else:
        raise NotImplementedError(f'"{args.stat}" is an unknown stat. Try "python player_stats.py rating"')
