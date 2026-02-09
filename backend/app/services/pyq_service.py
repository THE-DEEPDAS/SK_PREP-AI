import json
import random
import os
import re
import unicodedata

# ---------- PATH SETUP ----------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

PYQ_FILE = os.path.join(BASE_DIR, "scripts", "data", "pyq", "clean_pyq.json")


# ---------- TEXT CLEANER (IMPORTANT) ----------

def clean_text(text):

    if not text:
        return ""

    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)

    # Remove non-ascii garbage
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove OCR junk symbols
    text = re.sub(r'[~`^#@$%*_+=<>|]', ' ', text)

    # Remove repeated punctuation
    text = re.sub(r'[.]{2,}', '.', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)
    text = unicodedata.normalize("NFKC", text)

    # ---------------- STEP 2: Remove Invisible Unicode ----------------
    invisible_chars = [
        '\u200b',  # zero width space
        '\u200c',
        '\u200d',
        '\ufeff',  # BOM
        '\u2060',  # word joiner
        '\u00a0'   # non-breaking space
    ]

    for ch in invisible_chars:
        text = text.replace(ch, " ")

    # ---------------- STEP 3: Replace Smart Quotes ----------------

    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "-",
        "°": " degree ",
        "₹": " Rs ",
        "€": " Euro ",
        "£": " Pound "
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

   

    # ---------------- STEP 5: Remove Broken Mathematical Noise ----------------

    text = re.sub(r'[±×÷√≈≠≤≥∞∑∫∂]', ' ', text)

    # ---------------- STEP 6: Remove Non-English Noise ----------------
    # Keep letters, numbers, punctuation

    text = re.sub(r'[^\w\s.,:;?!()%\-"/]', ' ', text)


    return text.strip()


# ---------- LOAD ALL PYQS ----------

def load_all_pyqs():

    with open(PYQ_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Clean dataset immediately
    for q in data:

        q["question_text"] = clean_text(q.get("question_text", ""))

        # Clean options if present
        if "options" in q and isinstance(q["options"], list):
            q["options"] = [clean_text(opt) for opt in q["options"]]

    return data


# ---------- NORMALIZE PAPER TYPE ----------

def normalize_paper(exam_type, paper_type):

    # Prelims always mapped to "prelims"
    if exam_type.lower() == "prelims":
        return "prelims"

    # Mains keeps GS mapping
    return paper_type.lower()


# ---------- FILTER PYQS ----------

def get_filtered_pyqs(exam_type, paper_type, limit):

    pyqs = load_all_pyqs()

    normalized_request_paper = normalize_paper(exam_type, paper_type)

    filtered = []

    for q in pyqs:

        # Skip broken questions
        question_text = clean_text(q.get("question_text", ""))

        if len(question_text) < 20:
            continue

        if (
            q["exam_type"].lower() == exam_type.lower()
            and q["paper_type"].lower() == normalized_request_paper
        ):
            filtered.append(q)

    # Shuffle so every mock is different
    random.shuffle(filtered)

    return filtered[:limit]
