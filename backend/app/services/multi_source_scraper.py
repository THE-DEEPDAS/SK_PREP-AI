

# ============================================
# File: app/services/multi_source_scraper.py
# ============================================

class MultiSourcePYQScraper:
    """
    Scrape PYQ from multiple sources and merge
    """
    
    def __init__(self):
        self.sources = {
            "vision_ias": "https://www.visionias.in",
            "insights": "https://www.insightsonindia.com",
            "byju": "https://byjus.com/free-ias-prep/upsc-mains-previous-year-papers/",
            "unacademy": "https://unacademy.com/goal/upsc-civil-services-examination-ias",
            "drishti": "https://www.drishtiias.com/pyq"
        }
    
    async def scrape_all_sources(self, year: int) -> List[Dict]:
        """Scrape PYQ from all sources for a given year"""
        
        all_questions = []
        
        # Vision IAS
        try:
            questions = await self._scrape_vision_ias(year)
            all_questions.extend(questions)
        except Exception as e:
            logger.error(f"Vision IAS scraping failed: {e}")
        
        # Insights IAS
        try:
            questions = await self._scrape_insights(year)
            all_questions.extend(questions)
        except Exception as e:
            logger.error(f"Insights scraping failed: {e}")
        
        # Drishti IAS
        try:
            questions = await self._scrape_drishti(year)
            all_questions.extend(questions)
        except Exception as e:
            logger.error(f"Drishti scraping failed: {e}")
        
        # Remove duplicates
        unique_questions = self._deduplicate_questions(all_questions)
        
        return unique_questions
    
    async def _scrape_vision_ias(self, year: int) -> List[Dict]:
        """Scrape Vision IAS"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.sources['vision_ias']}/pyq/{year}"
            response = await client.get(url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            questions = []
            
            # Custom parsing logic for Vision IAS structure
            question_divs = soup.find_all('div', class_='question-block')
            
            for div in question_divs:
                q_text = div.find('p', class_='question')
                paper = div.find('span', class_='paper-tag')
                
                if q_text:
                    questions.append({
                        "question_text": q_text.text.strip(),
                        "year": year,
                        "paper": paper.text if paper else "Unknown",
                        "source": "Vision IAS"
                    })
            
            return questions
    
    async def _scrape_insights(self, year: int) -> List[Dict]:
        """Scrape Insights IAS"""
        # Similar implementation
        return []
    
    async def _scrape_drishti(self, year: int) -> List[Dict]:
        """Scrape Drishti IAS"""
        # Similar implementation
        return []
    
    def _deduplicate_questions(self, questions: List[Dict]) -> List[Dict]:
        """Remove duplicate questions using fuzzy matching"""
        
        from difflib import SequenceMatcher
        
        unique = []
        seen = set()
        
        for q in questions:
            # Check if similar question already exists
            is_duplicate = False
            q_text = q["question_text"].lower()
            
            for seen_text in seen:
                similarity = SequenceMatcher(None, q_text, seen_text).ratio()
                if similarity > 0.85:  # 85% similar = duplicate
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(q)
                seen.add(q_text)
        
        logger.info(f"Removed {len(questions) - len(unique)} duplicate questions")
        return unique