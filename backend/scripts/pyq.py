import sys
import re
import json
import asyncio
from pathlib import Path
from datetime import datetime

import pdfplumber
import PyPDF2
import pytesseract
from pdf2image import convert_from_path

# make backend importable
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.vector_service import VectorService


class PYQProcessor:
    def __init__(self, base_path="data/pyq"):
        self.base_path = Path(base_path)
        self.vector_service = None
        self.all_questions = []
        self.failed_pdfs = [] 
        self.output_file = Path("scripts/data/pyq/processed_pyq.json")

        self.existing_questions = []
        self.existing_keys = set()

        if self.output_file.exists():
            self.existing_questions = json.loads(self.output_file.read_text())

            for q in self.existing_questions:
                key = (
                    q["year"],
                    q["exam_type"],
                    q["paper_type"],
                    q.get("question_number"),
                    q["question_text"][:120]
                )
                self.existing_keys.add(key)

    # --------------------------------------------------
    # INIT VECTOR DB
    # --------------------------------------------------
    async def initialize(self):
        self.vector_service = VectorService()
        await self.vector_service.initialize()
        print("✓ Vector database initialized")

    # --------------------------------------------------
    # SAFE PDF TEXT EXTRACTION (NO OOM)
    # --------------------------------------------------
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        text = ""

        # 1️⃣ pdfplumber (best)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"  ⚠ pdfplumber failed: {e}")

        # 2️⃣ PyPDF2 fallback
        if len(text.strip()) < 200:
            try:
                with open(pdf_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"  ⚠ PyPDF2 failed: {e}")

        # 3️⃣ OCR fallback (PAGE BY PAGE → SAFE)
        if len(text.strip()) < 200:
            print(f"  ⚠ OCR fallback → {pdf_path.name}")
            try:
                reader = PyPDF2.PdfReader(open(pdf_path, "rb"))
                for i in range(len(reader.pages)):
                    images = convert_from_path(
                        pdf_path,
                        dpi=150,
                        first_page=i + 1,
                        last_page=i + 1
                    )
                    for img in images:
                        text += pytesseract.image_to_string(img, lang="eng")
            except Exception as e:
                print(f"  ✗ OCR failed: {e}")

        return text

    # --------------------------------------------------
    # QUESTION EXTRACTION
    # --------------------------------------------------
    def extract_questions_from_text(self, text, exam_type, paper_type, year):
        questions = []

        pattern = re.compile(
            r"(?:^|\n)\s*(\d{1,2})[\.\)]\s+(.*?)(?=\n\s*\d{1,2}[\.\)]|\Z)",
            re.DOTALL
        )

        for qno, qtext in pattern.findall(text):
            qtext = re.sub(r"\s+", " ", qtext).strip()
            if len(qtext) > 30:
                questions.append({
                    "question_number": int(qno),
                    "question_text": qtext[:1500],
                    "year": year,
                    "exam_type": exam_type,
                    "paper_type": paper_type,
                    "marks": self._estimate_marks(exam_type, paper_type),
                    "difficulty": self._estimate_difficulty(qtext),
                })

        return questions
    def extract_questions_fallback(self, text, exam_type, paper_type, year):
    questions = []
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 40]

    q_no = 1
    for line in lines:
        if any(word in line.lower() for word in [
            "discuss", "examine", "analyze", "critically",
            "evaluate", "comment", "explain", "elucidate"
        ]):
            questions.append({
                "question_number": q_no,
                "question_text": line[:1200],
                "year": year,
                "exam_type": exam_type,
                "paper_type": paper_type,
                "marks": self._estimate_marks(exam_type, paper_type),
                "difficulty": self._estimate_difficulty(line),
                "source": "OCR-fallback"
            })
            q_no += 1

    return questions
    def retry_failed_pdfs(self):
    print("\n🔁 Retrying failed PDFs...")
    print("=" * 60)

    recovered = 0

    for pdf_path in self.failed_pdfs:
        print(f"⚠ Retrying → {pdf_path.name}")

        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            continue

        year = self._extract_year(pdf_path.name)

        questions = self.extract_questions_fallback(
            text=text,
            exam_type="mains",
            paper_type="unknown",
            year=year
        )

        if questions:
            self.all_questions.extend(questions)
            recovered += len(questions)
            print(f"  ✓ Recovered {len(questions)}")
        else:
            print("  ✗ Still 0")

    print(f"\n✓ Total recovered via fallback: {recovered}")




    def _estimate_marks(self, exam_type, paper_type):
        if exam_type == "prelims":
            return 2
        if paper_type == "essay":
            return 125
        return 10

    def _estimate_difficulty(self, text):
        t = text.lower()
        if any(k in t for k in ["critically", "evaluate", "analyze", "examine"]):
            return "Hard"
        if any(k in t for k in ["discuss", "explain"]):
            return "Medium"
        return "Easy"

    def _extract_year(self, name):
        m = re.search(r"(20\d{2})", name)
        return int(m.group(1)) if m else datetime.now().year

    # --------------------------------------------------
    # PRELIMS
    # --------------------------------------------------
    def process_prelims(self):
        total = 0

        for sub, ptype in [("prelims", "prelims_gs"), ("csat", "csat")]:
            folder = self.base_path / "prelims" / sub
            if not folder.exists():
                continue

            for pdf in folder.glob("*.pdf"):
                text = self.extract_text_from_pdf(pdf)
                if not text:
                    continue

                qs = self.extract_questions_from_text(
                    text,
                    exam_type="prelims",
                    paper_type=ptype,
                    year=self._extract_year(pdf.name)
               )

                print(f"    ✓ {len(qs)} questions")
                for q in qs:
                    key = (
                    q["year"],
                    q["exam_type"],
                    q["paper_type"],
                    q.get("question_number"),
                    q["question_text"][:120]
                )

                           

                if key not in self.existing_keys:
                    self.existing_keys.add(key)
                    self.all_questions.append(q)
    
            total += len(qs)
        return total



    # --------------------------------------------------
    # MAINS GS + ESSAY
    # --------------------------------------------------
    def process_mains(self):
        total = 0
        base = self.base_path / "mains"

        for paper in ["gs1", "gs2", "gs3", "gs4", "essay"]:
            folder = base / paper
            if not folder.exists():
                continue

            for pdf in folder.glob("*.pdf"):
                year = self._extract_year(pdf.name)
                print(f"  {year}: {pdf.name}")
                text = self.extract_text_from_pdf(pdf)
                qs = self.extract_questions_from_text(text, "mains", paper, year)
                print(f"    ✓ {len(qs)} questions")
                self.all_questions.extend(qs)
                total += len(qs)

        return total

    # --------------------------------------------------
    # OPTIONAL (FLAT FOLDER)
    # --------------------------------------------------
    def process_optional(self):
        total = 0
        folder = self.base_path / "mains" / "optional"
        if not folder.exists():
            return 0

        SUBJECTS = [
            "geography", "history", "sociology", "anthropology",
            "political science", "public administration", "economics",
            "philosophy", "psychology", "law", "management",
        ]

        for pdf in folder.glob("*.pdf"):
            name = pdf.name.lower()
            year = self._extract_year(pdf.name)

            subject = "unknown"
            for s in SUBJECTS:
                if s.replace(" ", "") in name.replace(" ", ""):
                    subject = s.replace(" ", "_")
                    break

            paper = "paper1" if re.search(r"(paper[-_ ]?1|\bi\b)", name) else \
                    "paper2" if re.search(r"(paper[-_ ]?2|\bii\b)", name) else "unknown"

            print(f"  {year} | {subject} | {paper}: {pdf.name}")

            text = self.extract_text_from_pdf(pdf)
            qs = self.extract_questions_from_text(
                text, "mains", f"optional_{subject}_{paper}", year
            )

            print(f"    ✓ {len(qs)} questions")
            self.all_questions.extend(qs)
            total += len(qs)

        return total

    # --------------------------------------------------
    # SAVE + VECTOR LOAD
    # --------------------------------------------------
    def save_to_json(self):
    # Combine old + newly extracted questions
        final_questions = self.existing_questions + self.all_questions

    # Sort newest first
        final_questions = sorted(
        final_questions,
        key=lambda x: (x["year"], x.get("question_number", 0)),
        reverse=True
        )

    # Ensure folder exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write back to SAME JSON file
        self.output_file.write_text(
        json.dumps(final_questions, indent=2, ensure_ascii=False),
        encoding="utf-8"
        )

        print(f"✓ Saved {len(final_questions)} questions → {self.output_file}")



    


    async def load_vectors(self):
        texts, meta = [], []
        for q in self.all_questions:
            texts.append(f"{q['exam_type']} {q['paper_type']} {q['year']} Q{q['question_number']}: {q['question_text']}")
            meta.append(q)

        if texts:
            await self.vector_service.add_documents(texts, meta)
            print(f"✓ Loaded {len(texts)} vectors")

    # --------------------------------------------------
    # MAIN
    # --------------------------------------------------
    async def run(self):
        await self.initialize()

        print("\n📝 PRELIMS")
        p = self.process_prelims()

        print("\n📝 MAINS")
        m = self.process_mains()

        print("\n📝 OPTIONAL")
        o = self.process_optional()

        print("\n==============================")
        print(f"Prelims : {p}")
        print(f"Mains   : {m}")
        print(f"Optional: {o}")
        print(f"TOTAL   : {len(self.all_questions)}")
        print("==============================")

        self.save_to_json()
        await self.load_vectors()


if __name__ == "__main__":
    asyncio.run(PYQProcessor().run())
