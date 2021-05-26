from datetime import datetime
from time import sleep
from typing import List

import requests
from config import API_ENDPOINT, API_RPS, TOKEN
from pydantic import ValidationError
from schema.replay import Replay


class Balls:
    def __init__(self):
        self.headers = {
            'Authorization': TOKEN
        }
    
    def chase(self, id: str, date_limit: datetime=None) -> List[Replay]:
        sleep(1/API_RPS)
        payload = {
            'player-id': id,
            'playlist': 'private',
            'count': 200
        }

        if date_limit:
            payload['replay-date-before'] = f"{date_limit.strftime('%Y-%m-%d')}T03:22:25+02:00"
            print(f"fetching {payload['replay-date-before']}")
        
        resp = requests.get(API_ENDPOINT, params=payload, headers=self.headers)
        replays = []
        for r in resp.json().get('list', []):
            try:
                replays.append(Replay(**r))
            except ValidationError as e:
                print(f"{e}: https://ballchasing.com/replay/{r.get('id')}")
        
        return replays
    
    def chase_groups(self, group_id):
        sleep(1/API_RPS)
        payload = {
            'group': group_id,
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
