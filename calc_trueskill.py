import itertools
import math

import trueskill

from config import DRAW_PROBABILITY
from db import models, session

ENV = trueskill.TrueSkill(draw_probability=DRAW_PROBABILITY)

def win_probability(winners, losers):
    delta_mu = sum(r.mu for r in winners) - sum(r.mu for r in losers)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(winners, losers))
    size = len(winners) + len(losers)
    denom = math.sqrt(size * (ENV.beta * ENV.beta) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)


if __name__ == "__main__":
    new_rating = ENV.create_rating()
    for player in session.query(models.Player).all():
        player.rating = new_rating
    
    session.commit()

    replays = session.query(models.Replay).order_by(models.Replay.date.asc())
    
    for replay in replays:
        
        rating_groups = [
            { p.id: p.rating for p in replay.winners },
            { p.id: p.rating for p in replay.losers }
        ]

        quality = ENV.quality(rating_groups)

        rated_rating_groups = ENV.rate(rating_groups)
        for p in replay.winners:
            p.rating = rated_rating_groups[0][p.id]
        
        for p in replay.losers:
            p.rating = rated_rating_groups[1][p.id]
        
        replay.quality = quality
        replay.winner_chance = win_probability(replay.winners, replay.losers)

        session.commit()
        
        print(f"{replay.date} -- {replay.playlist_id} -- {round(quality*100)}% -- {round(replay.winner_chance*100)}%")
