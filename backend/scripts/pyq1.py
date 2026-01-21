import json
import re
from pathlib import Path
from datetime import datetime
import PyPDF2
from app.services.vector_service import VectorService

class PYQProcessor:
    def __init__(self, base_path="scripts/data/pyq"):
        self.base_path = Path(base_path)
        self.output_file = self.base_path / "processed_pyq.json"

        self.all_questions = []
        self.failed_pdfs = []

        # load existing questions (DEDUP SAFE)
        self.existing_questions = []
        self.existing_keys = set()

        if self.output_file.exists():
            data = json.loads(self.output_file.read_text())
            self.existing_questions = data
            for q in data:
                key = (
                    q["year"],
                    q["exam_type"],
                    q["paper_type"],
                    q.get("question_number"),
                    q["question_text"][:120]
                )
                self.existing_keys.add(key)

    # ----------------------------------------------------
    def extract_text(self, pdf_path):
        try:
            reader = PyPDF2.PdfReader(open(pdf_path, "rb"))
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            return text.strip()
        except:
            return ""

    # ----------------------------------------------------
    def extract_questions(self, text, year, exam, paper):
        questions = []

        patterns = [
            r"\n(\d+)\.\s+(.*?)(?=\n\d+\.|\Z)",            # 1.
            r"\n\((a|b|c|d|e)\)\s+(.*?)(?=\n\(|\Z)",       # (a)
            r"\n([ivxlcdm]+)\.\s+(.*?)(?=\n[ivxlcdm]+\.|\Z)", # i.
        ]

        for pat in patterns:
            for m in re.finditer(pat, text, re.I | re.S):
                qtext = m.group(2).strip()
                if len(qtext) < 30:
                    continue

                q = {
                    "year": year,
                    "exam_type": exam,
                    "paper_type": paper,
                    "question_number": m.group(1),
                    "question_text": " ".join(qtext.split()),
                }

                key = (
                    q["year"],
                    q["exam_type"],
                    q["paper_type"],
                    q["question_number"],
                    q["question_text"][:120]
                )

                if key not in self.existing_keys:
                    self.existing_keys.add(key)
                    questions.append(q)

        return questions

    # ----------------------------------------------------
    def process_folder(self, folder, exam, paper):
        count = 0

        for pdf in folder.glob("*.pdf"):
            year = self.extract_year(pdf.name)
            print(f"  {year} | {exam} | {pdf.name}")

            text = self.extract_text(pdf)
            if not text:
                print("    ⚠ skipped (no text)")
                self.failed_pdfs.append(str(pdf))
                continue

            qs = self.extract_questions(text, year, exam, paper)
            print(f"    ✓ {len(qs)} questions")

            self.all_questions.extend(qs)
            count += len(qs)

        return count

    # ----------------------------------------------------
    def extract_year(self, name):
        m = re.search(r"(20\d{2})", name)
        return int(m.group(1)) if m else datetime.now().year

    # ----------------------------------------------------
    def save(self):
        final = self.existing_questions + self.all_questions

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.output_file.write_text(json.dumps(final, indent=2))

        if self.failed_pdfs:
            (self.base_path / "failed_pdfs.txt").write_text(
                "\n".join(self.failed_pdfs)
            )

        print(f"\n✓ Saved {len(final)} questions → {self.output_file}")
        print(f"⚠ Failed PDFs saved → failed_pdfs.txt")

    # ----------------------------------------------------
    async def load_qdrant(self):
        if not self.all_questions:
            print("⚠ Skipping Qdrant insert (empty batch)")
            return

        vs = VectorService()
        await vs.initialize()

        texts = [q["question_text"] for q in self.all_questions]
        meta = [q for q in self.all_questions]

        await vs.add_documents(texts, meta)
        print(f"✓ Loaded {len(texts)} vectors")

    # ----------------------------------------------------
    async def run(self):
        print("\n📝 PRELIMS")
        p = self.base_path / "prelims"
        self.process_folder(p / "prelims", "prelims", "gs")
        self.process_folder(p / "csat", "prelims", "csat")

        print("\n📝 MAINS")
        m = self.base_path / "mains"
        for g in ["gs1", "gs2", "gs3", "gs4", "essay"]:
            self.process_folder(m / g, "mains", g)

        print("\n📝 OPTIONAL")
        self.process_folder(m / "optional", "optional", "optional")

        print("\n==============================")
        print(f"TOTAL NEW : {len(self.all_questions)}")
        print("==============================")

        self.save()
        await self.load_qdrant()
