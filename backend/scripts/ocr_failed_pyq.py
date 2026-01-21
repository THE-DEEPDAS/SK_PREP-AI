import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

FAILED = Path("scripts/data/pyq/failed_pdfs.txt")
OUT = Path("scripts/data/pyq/ocr_text")
OUT.mkdir(exist_ok=True)

for pdf in FAILED.read_text().splitlines():
    pdf = Path(pdf)
    print(f"OCR → {pdf.name}")

    images = convert_from_path(pdf, dpi=300)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    out_file = OUT / f"{pdf.stem}.txt"
    out_file.write_text(text)

    print("✓ done")
