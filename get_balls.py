from sqlalchemy.exc import IntegrityError

from config import GROUP_IDS
from core.balls import Balls
from core.match import Match
from core.skill import PrivateTrueSkill
from db import models, session

if __name__ == '__main__':
    balls = Balls()
    
    for group_id in GROUP_IDS:
        print(f"Fetching replays for {group_id}...", end=" ", flush=True)
        replays = balls.chase(group_id)
        print(f"{len(replays)} replays returned...", end=" ", flush=True)
        for i, r in enumerate(replays):
            m = Match(r)
            if m.group_member_count > 2 and r.duration >= 300:
                try:
                    replay = models.Replay(
                        id=r.id,
                        match_hash=m.match_hash,
                        replay_title=r.replay_title,
                        rocket_league_id=r.rocket_league_id,
                        link=f"https://ballchasing.com/replay/{r.id}",
                        playlist_id=r.playlist_id,
                        date=r.date,
                        duration=r.duration,
                        player_count=len(m.players)
                    )
                    session.add(replay)
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    continue
            else:
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
        print(f"Saved.", flush=True)
    
    print('Rating Matches...', end=" ", flush=True)
    pts = PrivateTrueSkill()
    pts.rate_matches()
    print('Complete!')
    session.close()        
