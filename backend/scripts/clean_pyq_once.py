import sys
import os
import json

# ---------------- ADD BACKEND TO PYTHON PATH ----------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# ---------------- NOW IMPORT APP MODULES ----------------

from app.services.pyq_service import clean_text


# ---------------- FILE PATHS ----------------

INPUT = "backend/scripts/data/pyq/processed_pyq.json"
OUTPUT = "backend/scripts/data/pyq/clean_pyq.json"


# ---------------- CLEAN DATA ----------------

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

for q in data:

    q["question_text"] = clean_text(q.get("question_text", ""))

    if "options" in q:
        q["options"] = [clean_text(opt) for opt in q["options"]]


with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


print("PYQ DATA CLEANED SUCCESSFULLY")
