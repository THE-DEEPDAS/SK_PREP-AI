import json
from pathlib import Path

RAW = Path("data/pyq_extracted/pyq_raw.json")
data = json.loads(RAW.read_text())

for item in data:
    print("YEAR:", item["year"])
    print("PAPER:", item["paper"])
    print("------ SAMPLE TEXT START ------")
    print(item["text"][:2000])   # first ~1–2 pages text
    print("------ SAMPLE TEXT END ------")
    break

exit()
