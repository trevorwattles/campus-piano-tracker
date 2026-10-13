# Campus Piano Tracker (AI + SQL)

A database of pianos on a campus (buildings, rooms, pianos, tunings, technicians, repair requests, student reservations) with a web UI that answers plain-English questions.

**Write-up (results, prompting strategies, cost): [post.md](post.md)** · More examples: [examples.md](examples.md)

## Files
- `post.md`: the project write-up (what worked, what didn't, strategy comparison, cost).
- `examples.md`: 9 more question → SQL → answer examples.
- `schema.png`: schema diagram, generated from `setup.sql` by `make_schema.py` (needs Graphviz).
- `setup.sql` / `setupData.sql`: schema and sample data.
- `pianos.sqlite`: the seeded SQLite database (same content as the two `.sql` files).
- `app/`: Flask web app. `pipeline.py` runs question → SQL → rows → answer, `prompts.py` holds the three prompting strategies, `db.py` runs the read-only queries, and `llm.py` makes the OpenAI calls and tracks cost.
- `run_eval.py` + `questions.json`: run every question through every strategy. Output is in `results/`.
- `.env.example`: variable names only. Never commit a real API key.

## Run
1. Put your key in `.env` (`OPENAI_API_KEY=...`; see `.env.example`).
2. `docker compose up --build`, then open http://localhost:8000
   (without Docker: `pip install -r requirements.txt && python app/server.py`)

The app rebuilds its working SQLite file from `setup.sql` + `setupData.sql` on every start. Model-generated SQL runs against a read-only connection and must be a single SELECT.

## Evaluate strategies
`python run_eval.py` runs `questions.json` through `zero_shot`, `single_domain` and `cross_domain` and writes JSON (SQL, rows, answer, tokens, cost) to `results/`.

## Paper
Chang, Shuaichen, and Eric Fosler-Lussier. "How to Prompt LLMs for Text-to-SQL: A Study in Zero-shot, Single-domain, and Cross-domain Settings." arXiv:2305.11853 (2023). https://arxiv.org/abs/2305.11853
