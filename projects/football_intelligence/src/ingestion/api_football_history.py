from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TeamHistoryRequest:
    team_id: int
    last: int=10

class ApiFootballHistoryAdapter:
    def __init__(self, client):
        self.client=client

    def recent_fixtures(self, team_id: int, last: int=10):
        if last < 1: raise ValueError("last must be >= 1")
        # Client is intentionally injected so credentials/network policy stay outside the core.
        return self.client.get("/fixtures", params={"team":team_id,"last":last})

    def team_history(self, team_id: int, last: int=10):
        payload=self.recent_fixtures(team_id,last)
        return payload.get("response", payload) if isinstance(payload,dict) else payload
