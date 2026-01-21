from typing import List, Dict, Optional

class PYQScraper:
    """
    Scrape PYQ questions from various sources:
    - Vision IAS
    - Insights IAS
    - Previous year papers PDFs
    """
    
    def __init__(self):
        self.sources = [
            "https://www.visionias.in/previous-year-questions",
            "https://www.insightsonindia.com/previous-year-question-papers"
        ]
    
    async def scrape_pyq_from_vision(self, year: int) -> List[Dict]:
        """Scrape PYQ from Vision IAS"""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"https://www.visionias.in/upsc-previous-year-questions/{year}"
                response = await client.get(url)
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                questions = []
                
                # Parse questions based on website structure
                question_divs = soup.find_all('div', class_='question-container')
                
                for idx, div in enumerate(question_divs):
                    question_text = div.find('div', class_='question-text')
                    paper_info = div.find('span', class_='paper-info')
                    
                    if question_text:
                        questions.append({
                            "id": f"pyq_{year}_{idx}",
                            "year": year,
                            "paper": paper_info.text if paper_info else "Unknown",
                            "question_text": question_text.text.strip(),
                            "source": "Vision IAS"
                        })
                
                return questions
                
        except Exception as e:
            print(f"Error scraping Vision IAS: {e}")
            return []
    
    async def extract_pyq_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract questions from UPSC official PDF"""
        
        import PyPDF2
        import re
        
        questions = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    # Pattern to match question numbers (Q1., 1., etc.)
                    question_pattern = r'(?:Q|Question)?\s*(\d+)\.\s*(.+?)(?=(?:Q|Question)?\s*\d+\.|$)'
                    
                    matches = re.finditer(question_pattern, text, re.DOTALL)
                    
                    for match in matches:
                        q_num = match.group(1)
                        q_text = match.group(2).strip()
                        
                        if len(q_text) > 20:  # Filter out false matches
                            questions.append({
                                "question_number": int(q_num),
                                "question_text": q_text,
                                "page": page_num + 1
                            })
            
            return questions
            
        except Exception as e:
            print(f"Error extracting from PDF: {e}")
            return []