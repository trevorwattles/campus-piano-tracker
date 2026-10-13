"""Run every question through every strategy and save results/ JSON (for the write-up)."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))
from dotenv import load_dotenv

load_dotenv()
import db
from pipeline import ask
from prompts import STRATEGIES

here = os.path.dirname(__file__)
db.init_db()
questions = json.load(open(os.path.join(here, "questions.json")))
os.makedirs(os.path.join(here, "results"), exist_ok=True)

for strategy in STRATEGIES:
    results = [ask(q, strategy) for q in questions]
    total = sum(r["cost_usd"] for r in results)
    print(f"{strategy}: {sum(1 for r in results if r['error'])} errors, ${total:.4f}")
    with open(os.path.join(here, "results", f"response_{strategy}_{int(time.time())}.json"), "w") as f:
        json.dump({"strategy": strategy, "results": results}, f, indent=2)
