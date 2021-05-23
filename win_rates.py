from db import session, models

if __name__ == "__main__":
    players = session.query(models.Player).all()
    for p in players:
        p_result = {
            'name': p.display_name,
            'games_played': p.games_played,
            'win_rate': round(p.wins/p.games_played, 3)
        }
        
        print(p_result)