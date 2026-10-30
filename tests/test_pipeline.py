import unittest, uuid
from pathlib import Path
from src.realtime_finance.generate import generate, write
from src.realtime_finance.processor import run

class PipelineTests(unittest.TestCase):
    def test_generation_is_deterministic(self): self.assertEqual(generate(100),generate(100))
    def test_idempotency_and_replay(self):
        root=Path("tests/.tmp")/str(uuid.uuid4()); root.mkdir(parents=True); data=root/"events.jsonl"; db=root/"state.db"; write(generate(1200),data)
        try:
            first=run(data,db); second=run(data,db); replay=run(data,db,True)
            self.assertGreater(first["processed"],1000); self.assertGreater(first["late"],0); self.assertEqual(second["processed"],first["processed"]); self.assertGreater(second.get("duplicate",0),1000); self.assertGreaterEqual(replay.get("replayed",0),1)
        finally:
            for p in root.glob("*"): p.unlink()
            root.rmdir()

if __name__=="__main__": unittest.main()
