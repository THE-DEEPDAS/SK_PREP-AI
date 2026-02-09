
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
import asyncio
from datetime import datetime
import re

class UPSCScraper:
    """
    Scrape UPSC official website for:
    - Exam notifications
    - Syllabus updates
    - Results
    - Important announcements
    """
    
    def __init__(self):
        self.base_url = "https://upsc.gov.in"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def fetch_exam_notifications(self) -> List[Dict]:
        """Scrape latest exam notifications from UPSC"""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/examinations/examination-notifications",
                    headers=self.headers
                )
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                notifications = []
                
                # Find notification table/list
                notification_items = soup.find_all('div', class_='notification-item')
                
                for item in notification_items[:10]:  # Get latest 10
                    title = item.find('a')
                    date_elem = item.find('span', class_='date')
                    
                    if title and date_elem:
                        notifications.append({
                            "title": title.text.strip(),
                            "url": self.base_url + title['href'] if title.has_attr('href') else None,
                            "date": date_elem.text.strip(),
                            "type": "notification"
                        })
                
                return notifications
                
        except Exception as e:
            print(f"Error scraping notifications: {e}")
            return []
    
    async def fetch_exam_calendar(self) -> List[Dict]:
        """Scrape exam calendar/schedule"""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/examinations/examination-schedule",
                    headers=self.headers
                )
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                calendar = []
                
                # Parse calendar table
                tables = soup.find_all('table')
                
                for table in tables:
                    rows = table.find_all('tr')[1:]  # Skip header
                    
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 3:
                            calendar.append({
                                "exam_name": cols[0].text.strip(),
                                "date": cols[1].text.strip(),
                                "status": cols[2].text.strip() if len(cols) > 2 else "Active"
                            })
                
                return calendar
                
        except Exception as e:
            print(f"Error scraping calendar: {e}")
            return []
    
    async def fetch_results(self) -> List[Dict]:
        """Scrape latest results"""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/examinations/results",
                    headers=self.headers
                )
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = []
                
                result_links = soup.find_all('a', href=re.compile(r'result', re.I))
                
                for link in result_links[:10]:
                    results.append({
                        "title": link.text.strip(),
                        "url": self.base_url + link['href'] if link.has_attr('href') else None,
                        "type": "result"
                    })
                
                return results
                
        except Exception as e:
            print(f"Error scraping results: {e}")
            return []
    
    async def fetch_admit_cards(self) -> List[Dict]:
        """Scrape admit card notifications"""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/examinations/admit-cards",
                    headers=self.headers
                )
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                admit_cards = []
                
                cards = soup.find_all('div', class_='admit-card-item')
                
                for card in cards:
                    link = card.find('a')
                    if link:
                        admit_cards.append({
                            "exam": link.text.strip(),
                            "url": self.base_url + link['href'] if link.has_attr('href') else None,
                            "type": "admit_card"
                        })
                
                return admit_cards
                
        except Exception as e:
            print(f"Error scraping admit cards: {e}")
            return []
