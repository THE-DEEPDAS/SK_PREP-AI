import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from pathlib import Path


class CurrentAffairsScraper:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent
        self.data_dir = BASE_DIR / "scripts" / "data" / "current_affairs"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.today = datetime.now().strftime("%Y%m%d")

        self.sources = [

            {
                "name": "PIB",
                "url": "https://pib.gov.in/RssMain.aspx?Mod=1&Lang=1"
            },

            {
                "name": "PRSIndia",
                "url": "https://prsindia.org/updates/rss.xml"
            },

            {
                "name": "TheHindu",
                "url": "https://www.thehindu.com/news/national/feeder/default.rss"
            },

            {
                "name": "IndianExpress",
                "url": "https://indianexpress.com/feed/"
            },

            {
                "name": "BusinessStandard",
                "url": "https://www.business-standard.com/rss/latest.rss"
            },

            {
                "name": "EconomicTimes",
                "url": "https://economictimes.indiatimes.com/rssfeedstopstories.cms"
            }
        ]


    # ================= CONTENT CLASSIFICATION =================

    def categorize_topic(self, text):

        t = text.lower()

        mapping = {

            "Polity": ["constitution", "supreme court", "parliament", "bill", "governance"],
            "Economy": ["economy", "gdp", "budget", "inflation", "bank", "fiscal"],
            "Environment": ["climate", "forest", "pollution", "wildlife"],
            "International": ["foreign", "bilateral", "summit", "treaty", "un"],
            "Science": ["technology", "ai", "space", "research", "isro"],
            "Social": ["health", "education", "women", "poverty", "nutrition"]
        }

        for cat, keys in mapping.items():
            if any(k in t for k in keys):
                return cat

        return "General"


    def identify_gs_tags(self, category):

        gs_map = {

            "Polity": ["GS2"],
            "International": ["GS2"],
            "Economy": ["GS3"],
            "Environment": ["GS3"],
            "Science": ["GS3"],
            "Social": ["GS1", "GS2"],
            "General": ["GS1"]
        }

        return gs_map.get(category, ["GS1"])


    def prelims_or_mains(self, text):

        t = text.lower()

        prelims_keys = ["scheme", "mission", "index", "committee", "launched"]
        mains_keys = ["impact", "challenges", "reforms", "debate", "implications"]

        p = any(k in t for k in prelims_keys)
        m = any(k in t for k in mains_keys)

        if p and m:
            return "both"
        if p:
            return "prelims"
        if m:
            return "mains"

        return "both"


    # ================= FETCH ARTICLE BODY =================

    def fetch_content(self, url):

        try:

            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10)

            soup = BeautifulSoup(r.text, "html.parser")

            paras = soup.find_all("p")

            text = " ".join(p.text for p in paras)

            return text.strip()

        except Exception:
            return ""


    # ================= SCRAPE RSS SOURCE =================

    def scrape_source(self, source):

        print("🔍 Scraping:", source["name"])

        feed = feedparser.parse(source["url"])

        articles = []

        for entry in feed.entries[:20]:

            content = self.fetch_content(entry.link)

            combined = entry.title + " " + content

            category = self.categorize_topic(combined)

            gs_tags = self.identify_gs_tags(category)

            relevance = self.prelims_or_mains(combined)

            articles.append({

                "title": entry.title,
                "summary": content[:600],
                "full_text": content,
                "category": category,              # Polity, Economy, Environment
                "gs_papers": gs_tags,             # ["GS2"], ["GS3"]
                "exam_relevance": relevance,        # prelims / mains / both
                "source": source,
                "url": entry.link,
                "published": entry.get("published", ""),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "language": "english"
})


        print("✓", source["name"], ":", len(articles))

        return articles


    # ================= MAIN RUN =================

    def run(self):

        for src in self.sources:

            articles = self.scrape_source(src)

            source_dir = self.data_dir / src["name"]
            source_dir.mkdir(exist_ok=True)

            outfile = source_dir / f"{self.today}.json"

            with open(outfile, "w", encoding="utf-8") as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)

            print("📁 Saved:", outfile)

        print("\n✅ DAILY SCRAPING COMPLETE")


if __name__ == "__main__":

    CurrentAffairsScraper().run()
