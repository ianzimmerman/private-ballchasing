import itertools
import math

import trueskill

from config import DRAW_PROBABILITY
from db import models, session


class PrivateTrueSkill:
    def __init__(self, env=None) -> None:
        self.env = env or trueskill.TrueSkill(draw_probability=DRAW_PROBABILITY)
    
    def new_rating(self):
        return self.env.create_rating()

    def win_probability(self, winners, losers):
        delta_mu = sum(r.mu for r in winners) - sum(r.mu for r in losers)
        sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(winners, losers))
        size = len(winners) + len(losers)
        denom = math.sqrt(size * (self.env.beta * self.env.beta) + sum_sigma)
        # ts = trueskill.global_env()
        return self.env.cdf(delta_mu / denom)

    def rate_matches(self):
        session.query(models.Player).update({
            models.Player.mu: self.new_rating().mu,
            models.Player.sigma: self.new_rating().sigma
        })
        session.commit()
    
        replay_query = session.query(models.Replay).order_by(models.Replay.date.asc())
        for replay in replay_query:
        
            rating_groups = [
                { p.id: p.rating for p in replay.winners },
                { p.id: p.rating for p in replay.losers }
            ]

            try:
                replay.quality = self.env.quality(rating_groups)
                replay.winner_chance = self.win_probability(replay.winners, replay.losers)
            
            except ValueError as e:
                print(e)
                continue
        
            rated_rating_groups = self.env.rate(rating_groups)
            for p in replay.winners:
                p.rating = rated_rating_groups[0][p.id]
            
            for p in replay.losers:
                p.rating = rated_rating_groups[1][p.id]
        
            session.commit()
