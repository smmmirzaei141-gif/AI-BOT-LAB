import json,time,requests,os
from datetime import datetime,timezone

API="https://api.hyperliquid.xyz/info"
COIN="BTC"
INTERVAL="1h"

TP=0.02
SL=0.01
FEE=0.0004
SLIPPAGE=0.0002
TIMEOUT_HOURS=24

SWEEP_LB=10
MSS_LB=5
MAX_MSS=2

STATE="projects/btc_bot/config/paper_state.json"
LOG="projects/btc_bot/config/paper_trades.jsonl"

def api(payload):
    r=requests.post(API,json=payload,timeout=15)
    r.raise_for_status()
    return r.json()

def candles():
    end=int(time.time()*1000)
    start=end-(200*60*60*1000)
    d=api({"type":"candleSnapshot","req":{
        "coin":COIN,"interval":INTERVAL,
        "startTime":start,"endTime":end}})
    d=sorted(d,key=lambda x:int(x["T"]))
    now=int(time.time()*1000)
    # فقط کندل‌های بسته‌شده
    return [
        {"t":int(x["T"]),"o":float(x["o"]),"h":float(x["h"]),
         "l":float(x["l"]),"c":float(x["c"])}
        for x in d if int(x["T"])+3600000 <= now
    ]

def price():
    d=api({"type":"allMids"})
    return float(d[COIN])

def ema(v,p):
    a=2/(p+1)
    e=v[0]
    for x in v[1:]:
        e=a*x+(1-a)*e
    return e

def regime(c,i):
    if i<55:
        return "UNKNOWN"

    closes=[x["c"] for x in c[:i]]
    e20=ema(closes[-40:],20)
    e50=ema(closes[-50:],50)
    sep=abs(e20-e50)/e50

    r=[]
    for j in range(max(1,i-24),i):
        r.append(abs(c[j]["c"]/c[j-1]["c"]-1))

    vol=sum(r)/len(r) if r else 0

    if vol>=0.012:
        return "HIGH_VOL"
    if sep>=0.004:
        return "TREND"
    return "RANGE"

def sweep(c,i):
    if i<SWEEP_LB:
        return None

    hi=max(x["h"] for x in c[i-SWEEP_LB:i])
    lo=min(x["l"] for x in c[i-SWEEP_LB:i])

    if c[i]["h"]>hi and c[i]["c"]<hi:
        return "BEARISH"

    if c[i]["l"]<lo and c[i]["c"]>lo:
        return "BULLISH"

    return None

def mss(c,i):
    if i<MSS_LB:
        return None

    hi=max(x["h"] for x in c[i-MSS_LB:i])
    lo=min(x["l"] for x in c[i-MSS_LB:i])

    if c[i]["c"]<lo:
        return "BEARISH"

    if c[i]["c"]>hi:
        return "BULLISH"

    return None

def load_state():
    if os.path.exists(STATE):
        try:
            with open(STATE) as f:
                return json.load(f)
        except:
            pass

    return {
        "last_candle":0,
        "sweep_index":None,
        "entry":None,
        "trades":0,
        "wins":0,
        "losses":0,
        "timeouts":0,
        "pnl":0.0
    }

def save(s):
    tmp=STATE+".tmp"
    with open(tmp,"w") as f:
        json.dump(s,f,indent=2)
    os.replace(tmp,STATE)

def log_trade(x):
    with open(LOG,"a") as f:
        f.write(json.dumps(x)+"\n")

def enter(s,c,i):
    ep=c[i]["c"]*(1-SLIPPAGE)

    s["entry"]={
        "time":c[i]["t"],
        "index":i,
        "price":ep,
        "tp":ep*(1-TP),
        "sl":ep*(1+SL)
    }

    print()
    print("="*75)
    print("PAPER SHORT ENTRY")
    print("Entry :",round(ep,2))
    print("TP    :",round(s["entry"]["tp"],2))
    print("SL    :",round(s["entry"]["sl"],2))
    print("Time  :",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*75)

def close_trade(s,result,exit_price):
    e=s["entry"]
    ep=e["price"]

    if result=="WIN":
        gross=(ep-exit_price)/ep
        p=gross-(2*FEE)
        s["wins"]+=1
    elif result=="LOSS":
        gross=(ep-exit_price)/ep
        p=gross-(2*FEE)
        s["losses"]+=1
    else:
        gross=(ep-exit_price)/ep
        p=gross-(2*FEE)
        s["timeouts"]+=1

    s["trades"]+=1
    s["pnl"]+=p

    log_trade({
        "time":datetime.now(timezone.utc).isoformat(),
        "side":"SHORT",
        "result":result,
        "entry":ep,
        "exit":exit_price,
        "pnl":p
    })

    print()
    print("PAPER EXIT:",result)
    print("Exit:",round(exit_price,2))
    print("PnL:",f"{p*100:+.2f}%")
    print(
        f"Stats T={s['trades']} "
        f"W={s['wins']} L={s['losses']} "
        f"TO={s['timeouts']} "
        f"PnL={s['pnl']*100:+.2f}%"
    )

    s["entry"]=None
    save(s)

def check_open(s):
    if not s["entry"]:
        return

    e=s["entry"]
    p=price()

    if p>=e["sl"]:
        close_trade(s,"LOSS",e["sl"])
        return

    if p<=e["tp"]:
        close_trade(s,"WIN",e["tp"])
        return

    age=(time.time()*1000-e["time"])/3600000

    if age>=TIMEOUT_HOURS:
        close_trade(s,"TIMEOUT",p)

def scan(s,c):
    if len(c)<60:
        return

    last=len(c)-1
    ts=c[last]["t"]

    if ts<=s["last_candle"]:
        return

    s["last_candle"]=ts
    save(s)

    print(
        datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M"),
        "CLOSE",round(c[last]["c"],2)
    )

    # اگر معامله باز داریم، Entry جدید ممنوع
    if s["entry"]:
        return

    # اگر Sweep قبلی داریم، MSS را فقط در دو کندل بعد بررسی کن
    si=s.get("sweep_index")

    if si is not None:
        bars=last-si

        if 1<=bars<=MAX_MSS:
            if mss(c,last)=="BEARISH":
                enter(s,c,last)
                s["sweep_index"]=None
                save(s)
                return

        if bars>MAX_MSS:
            s["sweep_index"]=None
            save(s)

    # Sweep جدید فقط در RANGE
    if sweep(c,last)=="BEARISH":
        if regime(c,last)=="RANGE":
            s["sweep_index"]=last
            save(s)

            print(
                "RANGE BEARISH SWEEP DETECTED",
                "| waiting for BEARISH MSS <=2"
            )

def main():
    print("="*75)
    print("V49 LIVE PAPER TRADING")
    print("BTC 1H | SHORT ONLY")
    print("BEARISH SWEEP -> MSS <=2 -> RANGE")
    print("TP=2% SL=1% TIMEOUT=24H")
    print("REAL ORDERS = OFF")
    print("="*75)

    s=load_state()

    while True:
        try:
            c=candles()

            check_open(s)
            scan(s,c)

            print(
                "NEXT CHECK |",
                datetime.now().strftime("%H:%M:%S"),
                "| Price",round(price(),2)
            )

            time.sleep(300)

        except KeyboardInterrupt:
            print("\nV49 PAPER STOPPED")
            save(s)
            break

        except Exception as e:
            print("ERROR:",e)
            time.sleep(30)

if __name__=="__main__":
    main()
