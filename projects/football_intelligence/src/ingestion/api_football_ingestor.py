from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from ..adapters.api_football import ApiFootballClient

@dataclass(frozen=True)
class FixtureBundle:
    fixture: dict[str, Any]
    lineups: list[dict[str, Any]]
    statistics: list[dict[str, Any]]
    events: list[dict[str, Any]]
    odds: list[dict[str, Any]]

class ApiFootballIngestor:
    def __init__(self, client: ApiFootballClient):
        self.client = client

    def collect(self, fixture_id: int) -> FixtureBundle:
        fixture_payload = self.client.fixtures(fixture=fixture_id)
        fixtures = fixture_payload.get("response", [])
        fixture = fixtures[0] if fixtures else {}
        lineups = self.client.lineups(fixture_id).get("response", [])
        statistics = self.client.statistics(fixture_id).get("response", [])
        events = self.client.events(fixture_id).get("response", [])
        odds = self.client.odds(fixture_id).get("response", [])
        return FixtureBundle(fixture, lineups, statistics, events, odds)
