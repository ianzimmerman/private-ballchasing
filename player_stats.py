from schema.replay import Player
from sqlalchemy import func, and_
import trueskill
from db import session, models
import argparse
from core.stats.player import PlayerStats
from tabulate import tabulate


ENV = trueskill.TrueSkill(draw_probability=0)
parser = argparse.ArgumentParser(description='Find some stats')
parser.add_argument('stat', metavar='S', type=str, help='rating, ')
parser.add_argument('--n', type=int, help='limit to lobbies with n players')
parser.add_argument('--min', type=int, help='limit to min x games played')
parser.add_argument('--p1', type=str, help='player 1')
parser.add_argument('--p2', type=str, help='player 2')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

    if args.stat == 'rating':
        q = session.query(models.Player)
        players = sorted(q.all(), key=ENV.expose, reverse=True)
        leaders = []
        for p in players:
            stats = PlayerStats(player_id=p.id).win_rate(args.players)

            if stats.get('games_played', 0) >= (args.min or 25):
                stats['display_name'] = p.display_name
                stats['trueskill'] = round(ENV.expose(p.rating),1)
                leaders.append(stats)
        

        print(tabulate(leaders, headers="keys", tablefmt="github"))
        
    elif args.stat == 'headsup':
        if all([args.p1, args.p2]):
            stats = PlayerStats(player_name=args.p1)
            print(tabulate([stats.head_2_head(args.p2)], headers="keys", tablefmt="github"))
        
        else:
            raise ValueError('needs p1 and p2 nicks')
    
    else:
        raise NotImplementedError(f'"{args.stat}" is an unknown stat. Try "python player_stats.py rating"')
