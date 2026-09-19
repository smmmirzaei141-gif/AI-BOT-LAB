from __future__ import annotations

import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class FootballDataClient:
    """football-data.org v4 client using X-Auth-Token from environment."""

    def __init__(self, token_env: str = "FOOTBALL_DATA_TOKEN"):
        self.token_env = token_env

    def get(self, path: str, **params):
        token = os.getenv(self.token_env, "")
        if not token:
            raise RuntimeError(f"Missing {self.token_env}")
        query = urlencode({k: v for k, v in params.items() if v is not None})
        url = "https://api.football-data.org/v4/" + path.lstrip("/")
        if query:
            url += "?" + query
        req = Request(url, headers={"X-Auth-Token": token})
        with urlopen(req, timeout=15) as response:
            return json.load(response)

    def matches(self, date_from=None, date_to=None, status=None):
        return self.get("matches", dateFrom=date_from, dateTo=date_to, status=status)

    def competition_matches(self, competition: str, date_from=None, date_to=None):
        return self.get(f"competitions/{competition}/matches", dateFrom=date_from, dateTo=date_to)

    def standings(self, competition: str):
        return self.get(f"competitions/{competition}/standings")
