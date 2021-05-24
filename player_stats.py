from sqlalchemy import func, and_
import trueskill
from db import session, models
import argparse
from core.stats import PlayerStats
from tabulate import tabulate


ENV = trueskill.TrueSkill(draw_probability=0)
parser = argparse.ArgumentParser(description='Find some stats')
parser.add_argument('stat', metavar='S', type=str, help='rating, ')
parser.add_argument('--players', type=int, help='limit to lobbies with x players')
parser.add_argument('--min', type=int, help='limit to min x games played')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

    if args.stat == 'rating':
        q = session.query(models.Player)
        players = sorted(q.all(), key=ENV.expose, reverse=True)
        leaders = []
        for p in players:
            stats = PlayerStats(p.id).win_rate(args.players)

            if stats.get('games_played', 0) >= (args.min or 25):
                stats['display_name'] = p.display_name
                stats['trueskill'] = round(ENV.expose(p.rating),1)
                leaders.append(stats)
        

        print(tabulate(leaders, headers="keys", tablefmt="github"))
        
            
    else:
        raise NotImplementedError(f'"{args.stat}" is an unknown stat. Try "python player_stats.py rating"')
