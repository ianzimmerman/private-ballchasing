from schema.replay import PlayerID, Replay
from typing import List
from config import API_ENDPOINT, API_RPS, TOKEN
import requests
from time import sleep

class Balls:
    def __init__(self, player_id: PlayerID):
        self.player: PlayerID = player_id
        self.headers = {
            'Authorization': TOKEN
        }
    
    def fetch(self) -> List[Replay]:
        sleep(1/API_RPS)
        payload = {
            'player-id': f"{self.player.platform}:{self.player.id}",
            'playlist': 'private'
        }
        resp = requests.get(API_ENDPOINT, params=payload, headers=self.headers)
        return [Replay(**r) for r in resp.json().get('list')]