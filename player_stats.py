from sqlalchemy import func, and_
import trueskill
from db import session, models
import argparse


ENV = trueskill.TrueSkill(draw_probability=0)
parser = argparse.ArgumentParser(description='Find some stats')
parser.add_argument('stat', metavar='S', type=str, help='performance, ')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

    if args.stat == 'rating':
        q = session.query(models.Player)
        players = [p for p in q if len(p.results) > 29]
        leaderboard = sorted(players, key=ENV.expose, reverse=True)
            
        for l in leaderboard:
            print(f"{l.display_name.ljust(20)}", end=" ")
            print(f"MMR: {str(round(ENV.expose(l.rating), 1)).rjust(4)}", end="  |  ")
            print(f"GP: {str(l.games_played).rjust(3)}", end="  |  ")

            wr = l.wins/l.games_played
            print(f"WR: {str(round(100*(wr))).rjust(3)}%", end="  |  ")

            print(f"eWR: {str(round(100*(l.expected_winrate))).rjust(3)}%", end="  |  ")

            wrae = (wr - l.expected_winrate)/l.expected_winrate
            print(f"WRaE: {str(round(100*(wrae))).rjust(3)}%")
    else:
        raise NotImplementedError(f'"{args.stat}" is an unknown stat. Try "python player_stats.py rating"')
