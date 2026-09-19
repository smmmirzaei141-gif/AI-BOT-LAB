from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class ApiFootballConfig:
    base_url: str = "https://v3.football.api-sports.io"
    api_key_env: str = "API_FOOTBALL_KEY"

    @property
    def api_key(self) -> str:
        key = os.getenv(self.api_key_env, "")
        if not key:
            raise RuntimeError(f"Missing {self.api_key_env}")
        return key


class ApiFootballClient:
    """Authorized API-Football client. Credentials stay in environment variables."""

    def __init__(self, config: ApiFootballConfig | None = None):
        self.config = config or ApiFootballConfig()

    def get(self, path: str, **params: Any) -> dict[str, Any]:
        query = urlencode({k: v for k, v in params.items() if v is not None})
        url = self.config.base_url.rstrip("/") + "/" + path.lstrip("/")
        if query:
            url += "?" + query
        req = Request(url, headers={"x-apisports-key": self.config.api_key})
        with urlopen(req, timeout=15) as response:
            return __import__("json").load(response)

    def fixtures(self, date: str | None = None, league: int | None = None, season: int | None = None):
        return self.get("/fixtures", date=date, league=league, season=season)

    def lineups(self, fixture: int):
        return self.get("/fixtures/lineups", fixture=fixture)

    def statistics(self, fixture: int):
        return self.get("/fixtures/statistics", fixture=fixture)

    def events(self, fixture: int):
        return self.get("/fixtures/events", fixture=fixture)

    def odds(self, fixture: int | None = None, bookmaker: int | None = None):
        return self.get("/odds", fixture=fixture, bookmaker=bookmaker)
