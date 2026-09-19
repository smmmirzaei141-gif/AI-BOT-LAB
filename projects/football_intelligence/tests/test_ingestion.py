from projects.football_intelligence.src.ingestion.pre_match_builder import build_input

class Bundle:
    fixture={"fixture":{"id":123},"teams":{"home":{"id":1,"name":"A"},"away":{"id":2,"name":"B"}}, "league":{"name":"Test League"}}

def test_build_input():
    x=build_input(Bundle())
    assert x.fixture_id==123
    assert x.league=="Test League"
