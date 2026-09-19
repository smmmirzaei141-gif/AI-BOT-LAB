from projects.football_intelligence.src.core.batch_backtest import run

def test_batch():
    cases=[1,2]
    def ev(c,edge):
        return [{"market":"goals","selection":"over_2.5","odds":2.0,"edge":.1,"won":c==1}]
    r=run(cases,ev,.04)
    assert r[0].bets==2 and r[0].wins==1 and r[0].profit==0
