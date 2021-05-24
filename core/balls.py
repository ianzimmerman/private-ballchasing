from time import sleep
from typing import List

import requests
from config import API_ENDPOINT, API_RPS, GROUP_IDS, TOKEN
from schema.replay import PlayerID, Replay


class Balls:
    def __init__(self):
        self.headers = {
            'Authorization': TOKEN
        }
    
    def fetch(self, id: str) -> List[Replay]:
        sleep(1/API_RPS)
        payload = {
            'player-id': id,
            'playlist': 'private'
        }
        resp = requests.get(API_ENDPOINT, params=payload, headers=self.headers)
        return [Replay(**r) for r in resp.json().get('list')]

    def chase(self) -> List[Replay]:
        replays = []
        for id in GROUP_IDS:
            replays.extend(self.fetch(id))
        
        return replays