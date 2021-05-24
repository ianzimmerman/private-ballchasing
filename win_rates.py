import trueskill
from db import session, models

ENV = trueskill.TrueSkill(draw_probability=0)

if __name__ == "__main__":
    players = session.query(models.Player).all()
    leaderboard = sorted(players, key=ENV.expose, reverse=True)
        
    for l in leaderboard:
        print(f"{l.display_name.ljust(20)} | GP: {str(l.games_played).ljust(6)}  WR: {round(100*(l.wins/l.games_played))}%, Rating: {round(ENV.expose(l.rating), 1)}")