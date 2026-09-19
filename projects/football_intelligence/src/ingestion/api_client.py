from __future__ import annotations
import os
import requests

class ApiFootballClient:
    def __init__(self, api_key: str|None=None, base_url="https://v3.football.api-sports.io"):
        self.api_key=api_key or os.getenv("API_FOOTBALL_KEY")
        if not self.api_key: raise RuntimeError("API_FOOTBALL_KEY is required")
        self.base_url=base_url.rstrip("/")

    def get(self,path,params=None):
        r=requests.get(self.base_url+path,headers={"x-apisports-key":self.api_key,"Accept":"application/json"},params=params,timeout=30)
        r.raise_for_status()
        return r.json()
