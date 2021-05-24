from sqlalchemy.exc import IntegrityError

from core.balls import Balls
from core.match import Match
from db import models, session
from schema.replay import PlayerID
from config import GROUP_IDS


if __name__ == '__main__':
    balls = Balls()
    
    for group_id in GROUP_IDS:
        replays = balls.chase(group_id)
        for i, r in enumerate(replays):
            m = Match(r)
            try:
                replay = models.Replay(
                    id=r.id,
                    rocket_league_id=r.rocket_league_id,
                    link=f"https://ballchasing.com/replay/{r.id}",
                    playlist_id=r.playlist_id,
                    date=r.date,
                    duration=r.duration,
                )
                session.add(replay)
                session.commit()
            except IntegrityError:
                session.rollback()
                continue

            for player in m.players:
                id_str = f"{player.id.platform}:{player.id.id}"
                p = session.query(models.Player).get(id_str)
                if not p:
                    p = models.Player(id=id_str)
                    session.add(p)
                    session.commit()
                
                a = session.query(models.Alias).filter(
                    models.Alias.player_id==id_str,
                    models.Alias.name==player.name
                ).first()

                if a:
                    a.count += 1
                else:
                    p.aliases.append(models.Alias(name=player.name))

                p.results.append(
                    models.PlayerResult(
                        match_win=m.player_won(player),
                        replay_id=r.id,
                        score=player.score,
                        start_time=player.start_time,
                        end_time=player.end_time
                    )
                )

                session.commit()

    session.close()        
