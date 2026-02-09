
def get_chat_prompt(query: str, context: str) -> str:
    """Generate chat prompt with context"""
    
    prompt = f"""You are an expert UPSC preparation assistant. Use the following context from study materials to answer the question.

Context from documents:
{context}

User Question: {query}

Instructions:
1. Provide accurate information based on the context
2. If the context doesn't contain the answer, say so clearly
3. Include relevant facts, dates, and examples
4. Structure your answer clearly
5. For UPSC preparation, focus on exam-relevant points

Answer:"""
    
    return prompt


def get_interview_evaluation_prompt(question: str, answer: str) -> str:
    """Generate prompt for interview evaluation"""
    
    prompt = f"""You are an experienced UPSC interview board member. Evaluate this candidate's response.

Question: {question}

Candidate's Answer: {answer}

Evaluate based on:
1. Content Quality (0-10): Depth, accuracy, relevance
2. Clarity (0-10): How well-articulated
3. Confidence (0-10): Based on language and structure

Provide:
- Overall Score (0-10)
- Detailed Feedback (3-4 sentences)
- 3 Strengths
- 3 Areas to Improve
- A relevant follow-up question

Format as JSON."""
    
    return prompt

