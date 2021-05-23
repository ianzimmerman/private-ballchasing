from os import name
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.selectable import Alias
from sqlalchemy.exc import IntegrityError
from schema.replay import PlayerID
from core.balls import Balls
from core.match import Match
from db import session, models
from config import PLAYER_ID, PLAYER_PLATFORM

MYID = PlayerID(
    platform=PLAYER_PLATFORM,
    id=PLAYER_ID
)


if __name__ == '__main__':
    b = Balls(MYID)
    replays = b.fetch()
    for i, r in enumerate(replays):
        m = Match(r)
        try:
            replay = models.Replay(
                id=r.id,
                rocket_league_id=r.rocket_league_id,
                playlist_id=r.playlist_id,
                date=r.date
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
                    replay_id=r.id
                )
            )

            session.commit()

    session.close()        
