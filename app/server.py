import os

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, render_template, request

import db
from pipeline import ask
from prompts import STRATEGIES

app = Flask(__name__)
db.init_db()

EXAMPLE_QUESTIONS = [
    "Which pianos need repair, and where are they?",
    "Which pianos have never been tuned?",
    "Who tuned the Steinway in the concert hall most recently?",
    "Which technicians are not certified, and which pianos did they tune?",
    "Which students have reported more than one repair request?",
    "How many pianos are in each building?",
]


@app.get("/")
def index():
    return render_template("index.html", strategies=STRATEGIES, examples=EXAMPLE_QUESTIONS,
                           schema=db.schema_sql())


@app.post("/api/ask")
def api_ask():
    body = request.get_json(force=True)
    question = (body.get("question") or "").strip()
    strategy = body.get("strategy", "single_domain")
    if not question or strategy not in STRATEGIES:
        return jsonify(error="A question and a valid strategy are required."), 400
    return jsonify(ask(question, strategy))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
