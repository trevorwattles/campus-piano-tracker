"""The three prompting strategies from https://arxiv.org/abs/2305.11853"""
import os

from db import schema_sql

SQL_REQUEST = (
    " Give me a sqlite select statement that answers the question. "
    "Only respond with sqlite syntax. If there is an error do not explain it! "
    "Prefer returning human-readable names (not just ids) so the result is understandable. "
    "Today's date is 2026-10-12."
)

with open(os.path.join(os.path.dirname(__file__), "dogshow_schema.sql")) as f:
    DOGSHOW_SCHEMA = f.read()

# Example pairs from this same database
SINGLE_DOMAIN_EXAMPLES = [
    ("Which pianos are in the Harris Fine Arts Center?",
     "SELECT p.piano_id, p.brand, p.model, r.room_number\n"
     "FROM piano p\nJOIN room r ON p.room_id = r.room_id\n"
     "JOIN building b ON r.building_id = b.building_id\n"
     "WHERE b.abbreviation = 'HFAC';"),
    ("Which pianos have never been tuned?",
     "SELECT p.piano_id, p.brand, p.model\nFROM piano p\n"
     "LEFT JOIN tuning t ON p.piano_id = t.piano_id\nWHERE t.tuning_id IS NULL;"),
]

# Example pair from a different database (the dog show example)
CROSS_DOMAIN_EXAMPLES = [
    ("Who doesn't have a way for us to text them?",
     "SELECT p.person_id, p.name\nFROM person p\n"
     "LEFT JOIN phone ph ON p.person_id = ph.person_id AND ph.can_recieve_sms = 1\n"
     "WHERE ph.phone_id IS NULL;"),
]

STRATEGIES = ["zero_shot", "single_domain", "cross_domain"]


def build_sql_prompt(strategy, question):
    schema = schema_sql()
    if strategy == "zero_shot":
        return f"{schema}\n{SQL_REQUEST}\nQuestion: {question}"
    if strategy == "single_domain":
        shots = "\n\n".join(f"Question: {q}\n{sql}" for q, sql in SINGLE_DOMAIN_EXAMPLES)
        return f"{schema}\nExamples for this database:\n{shots}\n{SQL_REQUEST}\nQuestion: {question}"
    if strategy == "cross_domain":
        shots = "\n\n".join(f"Question: {q}\n{sql}" for q, sql in CROSS_DOMAIN_EXAMPLES)
        return (f"Here is an example from a different database.\n{DOGSHOW_SCHEMA}\n{shots}\n\n"
                f"Now the real database:\n{schema}\n{SQL_REQUEST}\nQuestion: {question}")
    raise ValueError(f"unknown strategy {strategy}")


def build_answer_prompt(question, sql, columns, rows):
    shown = rows[:50]
    return (
        f'A user asked: "{question}"\n'
        f"This SQL was run against a campus piano database:\n{sql}\n"
        f"Columns: {columns}\nRows ({len(rows)} total, first {len(shown)} shown): {shown}\n\n"
        "Answer the user's question concisely in plain English using ONLY these rows. "
        "Read the rows carefully; don't reverse the meaning of the data. "
        "If the rows are empty, say no matching records were found. "
        "Do not add suggestions or chatter."
    )
