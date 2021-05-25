from time import sleep
from typing import List
from pydantic import ValidationError

import requests
from config import API_ENDPOINT, API_RPS, GROUP_IDS, TOKEN
from schema.replay import PlayerID, Replay


class Balls:
    def __init__(self):
        self.headers = {
            'Authorization': TOKEN
        }
    
    def chase(self, id: str) -> List[Replay]:
        sleep(1/API_RPS)
        payload = {
            'player-id': id,
            'playlist': 'private',
            'count': 200
        }
        resp = requests.get(API_ENDPOINT, params=payload, headers=self.headers)
        replays = []
        for r in resp.json().get('list', []):
            try:
                replays.append(Replay(**r))
            except ValidationError as e:
                print(f"{e}: https://ballchasing.com/replay/{r.get('id')}")
        
        return replays