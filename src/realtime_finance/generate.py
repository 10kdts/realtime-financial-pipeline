"""Gera eventos financeiros determinísticos, incluindo atraso e duplicidade controlados."""
from __future__ import annotations
import argparse, json, random
from datetime import datetime, timedelta, timezone
from pathlib import Path

def generate(count: int = 1200, seed: int = 42) -> list[dict]:
    rng=random.Random(seed); start=datetime(2026,1,1,tzinfo=timezone.utc); events=[]
    for i in range(count):
        occurred=start+timedelta(seconds=i*7)
        amount=round(min(rng.lognormvariate(4.1,1.0),12000),2)
        event={"event_id":f"evt-{i+1:07d}","account_id":f"acc-{rng.randint(1,180):04d}","occurred_at":occurred.isoformat().replace("+00:00","Z"),"received_at":(occurred+timedelta(seconds=rng.randint(0,25))).isoformat().replace("+00:00","Z"),"amount":amount,"type":rng.choice(["pix","card","transfer"]),"country":"INT" if rng.random()<.04 else "BR"}
        events.append(event)
    # atraso, fora de ordem e duplicidade são parte do cenário de teste
    if count > 800:
        delayed=dict(events[117]); delayed["event_id"]="evt-late-0001"; delayed["received_at"]=(start+timedelta(hours=4)).isoformat().replace("+00:00","Z"); events.append(delayed)
        events.extend([dict(events[25]),dict(events[25]),dict(events[800])])
    rng.shuffle(events)
    return sorted(events,key=lambda e:e["received_at"])

def write(events:list[dict],path:Path)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("\n".join(json.dumps(e,ensure_ascii=False) for e in events)+"\n",encoding="utf-8")

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--rows",type=int,default=1200); p.add_argument("--output",type=Path,default=Path("data/sample/events.jsonl")); a=p.parse_args(); events=generate(a.rows); write(events,a.output); print(f"{len(events)} eventos gravados em {a.output}")

