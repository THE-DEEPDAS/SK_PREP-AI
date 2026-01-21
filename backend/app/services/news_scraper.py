import asyncio
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from app.services.llm_service import LLMService   # ✅ IMPORTANT


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
                    response = await client.get(source, timeout=10)
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Adjust selector per website if needed
                    headlines = soup.find_all("h2", class_="title")[:5]

                    for headline in headlines:

                        news_text = headline.text.strip()

                        # 🔥 AI Classification
                        classification = await self.categorize_news(news_text)

                        articles.append({
                            "title": news_text,
                            "source": source,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "ai_classification": classification
                        })

                except Exception as e:
                    print(f"Error fetching {source}: {e}")

        return articles

    # ================= AI CLASSIFIER =================

    async def categorize_news(self, article: str):

        llm = LLMService()

        prompt = f"""
You are a UPSC examiner.

Classify the news strictly for UPSC exam usage.

Return ONLY JSON:

category → Polity/Economy/Environment/IR/Science/Social
gs_paper → GS1/GS2/GS3/GS4
relevance → prelims/mains/both

News:
{article}
"""

        response = await llm.generate_response(
            query=prompt,
            context=[],
            use_gpt4=False
        )

        return response


# ================= MAIN RUNNER =================

async def main():

    scraper = NewsScraper()
    articles = await scraper.fetch_daily_news()

    print("\nSCRAPED ARTICLES:\n")

    for a in articles:
        print(a)


if __name__ == "__main__":
    asyncio.run(main())
