import asyncio
from datetime import datetime
from typing import List, Dict


class SchedulerService:

    def __init__(self):
        self.exam_calendar = self._load_exam_calendar()
        self.running = False

    def _load_exam_calendar(self) -> List[Dict]:
        return [
            {
                "name": "UPSC Prelims 2025",
                "date": datetime(2025, 5, 26),
                "notify_before": [180, 90, 60, 30, 15, 7, 3, 1]
            },
            {
                "name": "UPSC Mains 2025",
                "date": datetime(2025, 9, 15),
                "notify_before": [180, 90, 60, 30, 15, 7, 3, 1]
            }
        ]

    async def start(self):
        print("✓ Scheduler started (async native)")
        self.running = True

        asyncio.create_task(self.daily_quote_loop())
        asyncio.create_task(self.weekly_summary_loop())
        asyncio.create_task(self.exam_alert_loop())
        asyncio.create_task(self.news_update_loop())

    # ---------------- TASK LOOPS ---------------- #

    async def daily_quote_loop(self):
        while self.running:
            now = datetime.now()

            if now.hour == 7 and now.minute == 0:
                await self.send_daily_quote()
                await asyncio.sleep(60)

            await asyncio.sleep(30)

    async def weekly_summary_loop(self):
        while self.running:
            now = datetime.now()

            if now.weekday() == 6 and now.hour == 20 and now.minute == 0:
                await self.send_weekly_summary()
                await asyncio.sleep(60)

            await asyncio.sleep(30)

    async def exam_alert_loop(self):
        while self.running:
            await self.check_exam_notifications()
            await asyncio.sleep(86400)  # once per day

    async def news_update_loop(self):
        while self.running:
            now = datetime.now()

            if now.hour == 9 and now.minute == 0:
                await self.fetch_daily_news()
                await asyncio.sleep(60)

            await asyncio.sleep(30)

    # ---------------- TASK FUNCTIONS ---------------- #

    async def send_daily_quote(self):
        print("📢 Daily quote sent")

    async def send_weekly_summary(self):
        print("📊 Weekly summary sent")

    async def check_exam_notifications(self):
        today = datetime.now().date()

        for exam in self.exam_calendar:
            days_left = (exam["date"].date() - today).days

            if days_left in exam["notify_before"]:
                print(f"🚨 Exam Alert: {exam['name']} in {days_left} days")

    async def fetch_daily_news(self):
        print("📰 Fetching current affairs...")