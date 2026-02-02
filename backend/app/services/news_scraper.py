import asyncio
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import json

from app.services.llm_service import LLMService


class NewsScraper:

    def __init__(self):
        self.sources = [
            "https://www.thehindu.com/news/national/",
            "https://indianexpress.com/section/india/",
            "https://pib.gov.in/allRel.aspx"
        ]

    # ================= FETCH NEWS =================

    async def fetch_daily_news(self) -> List[Dict]:

        articles = []

        async with httpx.AsyncClient() as client:

            for source in self.sources:

                try:
                    response = await client.get(source, timeout=15)
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Universal selector
                    headlines = soup.find_all("h2")[:5]

                    for headline in headlines:

                        news_text = headline.text.strip()

                        if not news_text:
                            continue

                        classification = await self.categorize_news(news_text)

                        articles.append({
                            "title": news_text,
                            "source": source,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "ai_classification": classification
                        })

                except Exception as e:
                    print(f"SCRAPER ERROR {source}:", e)

        return articles

    # ================= AI CLASSIFIER =================

    async def categorize_news(self, article: str):

        llm = LLMService()

        prompt = f"""
You are a UPSC examiner AI.

Classify this news.

Return ONLY VALID JSON.

FORMAT:

{{
  "category": "Polity/Economy/Environment/IR/Science/Social",
  "gs_paper": "GS1/GS2/GS3/GS4",
  "relevance": "prelims/mains/both"
}}

News:
{article}
"""

        response = await llm.generate_response(
            query=prompt,
            context=[]
        )

        print("RAW LLM RESPONSE:", response)

        # ---------- SAFETY FALLBACK ----------

        if not response:
            return {
                "category": "General",
                "gs_paper": "GS2",
                "relevance": "mains"
            }

        # ---------- JSON VALIDATION ----------

        try:
            parsed = json.loads(response)
            return parsed

        except Exception:
            print("JSON PARSE FAILED — FALLBACK USED")

            return {
                "category": "General",
                "gs_paper": "GS2",
                "relevance": "mains"
            }


# ================= MAIN RUNNER =================

async def main():

    scraper = NewsScraper()
    articles = await scraper.fetch_daily_news()

    print("\nSCRAPED ARTICLES:\n")

    for a in articles:
        print(a)


if __name__ == "__main__":
    asyncio.run(main())