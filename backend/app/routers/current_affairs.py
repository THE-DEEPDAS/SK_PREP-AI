from fastapi import APIRouter, Query
from pathlib import Path
from datetime import datetime
import json

# ================= ROUTER =================

router = APIRouter(
    prefix="/current-affairs",
    tags=["current_affairs"]
)

print(">>> CURRENT AFFAIRS ROUTER LOADED")

# ================= PATH =================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "scripts" / "data" / "current_affairs"

print("📂 DATA PATH:", DATA_DIR)


# ================= SAFE JSON READER =================

def safe_read_json(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data

            return []

    except Exception as e:
        print("JSON READ ERROR:", file_path.name, e)
        return []


# ================= LOAD ARTICLES =================

def load_articles(date: str):

    date_key = date.replace("-", "")

    all_articles = []
    seen_titles = set()

    if not DATA_DIR.exists():
        print("❌ DATA DIRECTORY MISSING")
        return []

    # loop sources
    for source_dir in DATA_DIR.iterdir():

        if not source_dir.is_dir():
            continue

        file_path = source_dir / f"{date_key}.json"

        # Load exact date only (NO FALLBACK)
        if file_path.exists():

            articles = safe_read_json(file_path)

            for art in articles:

                title = art.get("title", "").strip()

                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_articles.append(art)

    print("✅ FINAL ARTICLES:", len(all_articles))
    return all_articles


# ================= ARTICLES API =================

@router.get("/articles")
async def get_articles(
    date: str = Query(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
):

    articles = load_articles(date)

    return {
        "success": True,
        "count": len(articles),
        "articles": articles
    }


# ================= STATS API =================

@router.get("/stats")
async def get_stats(
    date: str = Query(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
):

    try:

        articles = load_articles(date)

        category_count = {}
        source_count = {}

        for article in articles:

            # category / tags
            tags = article.get("tags") or article.get("category") or []

            if isinstance(tags, list):
                for tag in tags:
                    category_count[tag] = category_count.get(tag, 0) + 1

            # source
            src = article.get("source", "Unknown")
            source_count[src] = source_count.get(src, 0) + 1

        return {
            "success": True,
            "total_articles": len(articles),
            "category_distribution": category_count,
            "source_distribution": source_count
        }

    except Exception as e:

        print("STATS ERROR:", e)

        return {
            "success": False,
            "total_articles": 0,
            "category_distribution": {},
            "source_distribution": {}
        }


# ================= SEARCH API =================

@router.get("/search")
async def search_articles(
    q: str,
    date: str = Query(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
):

    q = q.lower()

    articles = load_articles(date)

    results = [
        a for a in articles
        if q in a.get("title", "").lower()
        or q in a.get("summary", "").lower()
    ]

    return {
        "success": True,
        "query": q,
        "count": len(results),
        "results": results
    }


# ================= HEALTH =================

@router.get("/health")
async def health():

    return {
        "status": "ok",
        "time": datetime.now().isoformat()
    }
