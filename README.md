# Campus Piano Tracker (AI + SQL)

A database of pianos on a campus (buildings, rooms, pianos, tunings, technicians, repair requests, student reservations) with a web UI that answers plain-English questions.

## Run
1. Put your key in `.env` (`OPENAI_API_KEY=...`; see `.env.example`).
2. `docker compose up --build`, then open http://localhost:8000
   (without Docker: `pip install -r requirements.txt && python app/server.py`)

The SQLite file lives inside the container and is rebuilt from `setup.sql` + `setupData.sql` on every start. Model-generated SQL runs against a read-only connection and must be a single SELECT.

## Evaluate strategies
`python run_eval.py` runs `questions.json` through `zero_shot`, `single_domain` and `cross_domain` and writes JSON (SQL, rows, answer, tokens, cost) to `results/`.
