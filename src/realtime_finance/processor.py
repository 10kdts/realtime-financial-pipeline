"""Processador reexecutável com deduplicação, watermark, janelas e replay."""
from __future__ import annotations
import argparse, json, sqlite3
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path

def ts(value:str)->datetime: return datetime.fromisoformat(value.replace("Z","+00:00"))

class Processor:
    def __init__(self,db:Path,allowed_lateness_seconds:int=90):
        db.parent.mkdir(parents=True,exist_ok=True); self.conn=sqlite3.connect(db); self.lateness=timedelta(seconds=allowed_lateness_seconds); self.windows=defaultdict(deque); self.max_event_time=None
        self.conn.executescript("""CREATE TABLE IF NOT EXISTS processed_events(event_id TEXT PRIMARY KEY, occurred_at TEXT NOT NULL, amount REAL NOT NULL); CREATE TABLE IF NOT EXISTS alerts(alert_id TEXT PRIMARY KEY, event_id TEXT NOT NULL, reason TEXT NOT NULL, amount REAL NOT NULL); CREATE TABLE IF NOT EXISTS late_events(event_id TEXT PRIMARY KEY, occurred_at TEXT NOT NULL, watermark TEXT NOT NULL);""")
        latest=self.conn.execute("SELECT MAX(occurred_at) FROM processed_events").fetchone()[0]
        self.max_event_time=ts(latest) if latest else None
    def seen(self,event_id:str)->bool: return self.conn.execute("SELECT 1 FROM processed_events WHERE event_id=?",(event_id,)).fetchone() is not None
    def process(self,event:dict)->str:
        if self.seen(event["event_id"]): return "duplicate"
        occurred=ts(event["occurred_at"]); self.max_event_time=max(self.max_event_time or occurred,occurred); watermark=self.max_event_time-self.lateness
        if occurred<watermark:
            self.conn.execute("INSERT OR IGNORE INTO late_events VALUES(?,?,?)",(event["event_id"],event["occurred_at"],watermark.isoformat())); return "late"
        account=event["account_id"]; window=self.windows[account]
        while window and window[0][0]<occurred-timedelta(minutes=5): window.popleft()
        window.append((occurred,float(event["amount"])))
        reasons=[]
        if float(event["amount"])>=3000: reasons.append("high_amount")
        if len(window)>=6: reasons.append("velocity_5m")
        if event["country"]!="BR": reasons.append("international")
        self.conn.execute("INSERT INTO processed_events VALUES(?,?,?)",(event["event_id"],event["occurred_at"],event["amount"]))
        for reason in reasons: self.conn.execute("INSERT OR IGNORE INTO alerts VALUES(?,?,?,?)",(f'{event["event_id"]}:{reason}',event["event_id"],reason,event["amount"]))
        return "alert" if reasons else "processed"
    def replay_late(self,events_by_id:dict[str,dict])->int:
        ids=[r[0] for r in self.conn.execute("SELECT event_id FROM late_events")]; count=0
        for event_id in ids:
            event=events_by_id[event_id]
            if not self.seen(event_id):
                self.conn.execute("INSERT INTO processed_events VALUES(?,?,?)",(event_id,event["occurred_at"],event["amount"])); count+=1
        self.conn.commit(); return count
    def metrics(self)->dict:
        return {"processed":self.conn.execute("SELECT COUNT(*) FROM processed_events").fetchone()[0],"alerts":self.conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0],"late":self.conn.execute("SELECT COUNT(*) FROM late_events").fetchone()[0]}

def run(input_path:Path,db:Path,replay:bool=False)->dict:
    events=[json.loads(line) for line in input_path.read_text(encoding="utf-8").splitlines() if line]; p=Processor(db); counts=defaultdict(int)
    for event in events: counts[p.process(event)]+=1
    p.conn.commit()
    if replay: counts["replayed"]=p.replay_late({e["event_id"]:e for e in events})
    result={**dict(counts),**p.metrics()}; p.conn.close(); return result

if __name__=="__main__":
    a=argparse.ArgumentParser(); a.add_argument("--input",type=Path,default=Path("data/sample/events.jsonl")); a.add_argument("--db",type=Path,default=Path("data/pipeline.db")); a.add_argument("--replay",action="store_true"); x=a.parse_args(); print(json.dumps(run(x.input,x.db,x.replay),indent=2))

