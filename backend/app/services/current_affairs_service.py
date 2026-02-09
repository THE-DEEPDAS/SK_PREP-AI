import json
import glob
import os

# Root current affairs folder
CA_ROOT = "scripts/data/current_affair"


def load_all_current_affairs():

    all_articles = []

    # Loop through each source folder
    source_folders = glob.glob(f"{CA_ROOT}/*")

    for folder in source_folders:

        json_files = glob.glob(os.path.join(folder, "*.json"))

        for file in json_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if isinstance(data, list):
                        all_articles.extend(data)

            except Exception as e:
                print("CA LOAD ERROR:", file, e)

    return all_articles


def filter_current_affairs(exam_type, paper_type, limit=10):

    articles = load_all_current_affairs()

    filtered = []

    for a in articles:

        # Handle AI classified structure
        classification = a.get("ai_classification")

        if not classification:
            continue

        try:
            cls = json.loads(classification) if isinstance(classification, str) else classification
        except:
            continue

        relevance = cls.get("relevance", "")
        gs_paper = cls.get("gs_paper", "")

        # Filter prelims / mains
        if relevance not in [exam_type, "both"]:
            continue

        # Filter GS mapping
        if relevance.lower() not in [exam_type.lower(), "both"]:

            continue

        filtered.append({
            "title": a.get("title", ""),
            "summary": a.get("summary", ""),
            "source": a.get("source", ""),
            "category": cls.get("category", "")
        })

    return filtered[:limit]
load_current_affairs = load_all_current_affairs
