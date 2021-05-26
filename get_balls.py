import argparse
# from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from config import GROUP_IDS, MEMBER_IDS
from core.balls import Balls
from core.match import Match
# from core.skill import PrivateTrueSkill
from db import models, session

# months_to_grab = 18
# date_today = datetime(2021, 5, 25)
# delta = timedelta(days=30)

# dates = [date_today-(n*delta) for n in range(months_to_grab)]
# print(dates)


parser = argparse.ArgumentParser(description='chase some balls')
parser.add_argument('method', type=str, choices=['members', 'groups'])
parser.add_argument('--min_members', type=int, help="at least how many members should be present?")

if __name__ == '__main__':
    args = parser.parse_args()
    print(' ')
    print(args.method)
    print(' ')

    balls = Balls()
    chase_list = MEMBER_IDS if args.method == 'members' else GROUP_IDS
    
    for id in chase_list:
        print(f"Fetching replays for {id}...", end=" ", flush=True)
        if args.method == 'members':
            replays = balls.chase(id)
        elif args.method == 'groups':
            replays = balls.chase_groups(id)

        print(f"{len(replays)} replays returned...", end=" ", flush=True)

        valid_replays = 0
        for r in replays:
            m = Match(r, args.min_members)
            if m.is_valid:
                replay = session.query(models.Replay).filter(models.Replay.match_hash==m.match_hash).first()
                if replay:
                    continue
                else:
                    replay = models.Replay(
                        id=r.id,
                        match_hash=m.match_hash,
                        replay_title=r.replay_title,
                        rocket_league_id=r.rocket_league_id,
                        link=f"https://ballchasing.com/replay/{r.id}",
                        playlist_id=r.playlist_id,
                        date=r.date,
                        duration=r.duration,
                        player_count=len(m.players),
                        member_count=m.group_member_count
                    )
                    session.add(replay)
                    session.commit()
                    valid_replays += 1
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
        print(f"{valid_replays} replays Saved.", flush=True)
    
    # print('Rating Matches...', end=" ", flush=True)
    # pts = PrivateTrueSkill()
    # pts.rate_matches(args.min_members)
    # print('Complete!')
    session.close()
