from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PlayerID(BaseModel):
    platform: str
    id: str

class Player(BaseModel):
    name: str
    id: PlayerID
    score: int
    start_time: float
    end_time: float

class Team(BaseModel):
    name: Optional[str]
    goals: Optional[int]
    players: List[Player]

class Replay(BaseModel):
    id: str
    match_hash: Optional[int]
    replay_title: str
    link: str
    rocket_league_id: str
    playlist_id: str
    date: datetime
    blue: Team
    orange: Team
    duration: int

'''
{
      "id": "4e1d1949-717b-4636-95bb-673a0478cdf8",
      "link": "https://ballchasing.com/api/replays/4e1d1949-717b-4636-95bb-673a0478cdf8",
      "rocket_league_id": "ECAF212F4E9154C5F5C2F681C5D891EE",
      "replay_title": "NV vs SSG - 4 2021-04-12.01.26",
      "map_code": "utopiastadium_dusk_p",
      "map_name": "Utopia Coliseum (Dusk)",
      "playlist_id": "private",
      "playlist_name": "Private",
      "duration": 394,
      "overtime": true,
      "overtime_seconds": 60,
      "season": 3,
      "season_type": "free2play",
      "date": "2021-04-12T01:26:47Z",
      "date_has_tz": false,
      "visibility": "public",
      "created": "2021-04-15T15:37:41.876744+02:00",
      "uploader": {
        "steam_id": "76561198141161044",
        "name": "Can't Fly",
        "profile_url": "https://steamcommunity.com/id/cantflyrl/",
        "avatar": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/2e/2e988d06c9935eb54b09488ef0b03d94f9c157f0.jpg"
      },
      "groups": [
        {
          "id": "series-7-spacestation-4-3-envy-n4494gth36",
          "name": "Series 7 | Spacestation 4-3 Envy",
          "link": "https://ballchasing.com/api/groups/series-7-spacestation-4-3-envy-n4494gth36"
        }
      ],
      "blue": {
        "name": "TEAM ENVY",
        "goals": 1,
        "players": [
          {
            "start_time": 0,
            "end_time": 394.68646,
            "name": "mist",
            "id": {
              "platform": "steam",
              "id": "76561198245238200"
            },
            "score": 526
          },
          {
            "start_time": 0,
            "end_time": 394.68646,
            "name": "Atomic",
            "id": {
              "platform": "steam",
              "id": "76561198994386260"
            },
            "score": 238
          },
          {
            "start_time": 0,
            "end_time": 394.68646,
            "name": "TURBOPOLSA",
            "id": {
              "platform": "steam",
              "id": "76561198194977850"
            },
            "score": 226
          }
        ]
      },
      "orange": {
        "name": "SSG",
        "goals": 2,
        "players": [
          {
            "start_time": 0,
            "end_time": 394.68646,
            "name": "Sypical",
            "id": {
              "platform": "steam",
              "id": "76561198323843523"
            },
            "mvp": true,
            "score": 708
          },
          {
            "start_time": 0,
            "end_time": 394.68646,
            "name": "Arsenal",
            "id": {
              "platform": "steam",
              "id": "76561198368482029"
            },
            "score": 395
          },
          {
            "start_time": 0,
            "end_time": 394.68646,
            "name": "retals",
            "id": {
              "platform": "steam",
              "id": "76561198353975600"
            },
            "score": 301
          }
        ]
      }
    }
'''