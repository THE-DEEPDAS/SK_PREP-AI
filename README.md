🚀 UPSC ScholarAI — AI Powered Civil Services Preparation Platform

An intelligent AI-driven learning platform for UPSC aspirants featuring AI Chat Assistant, Mock Test Generator, Current Affairs Analyzer, PYQ Practice, and Interview Preparation — all in one unified dashboard.🌟 Features



🤖 AI UPSC Assistant
Context-aware chatbot for UPSC syllabus queries
Prelims & Mains oriented answers
Source-based response generation
Uses OpenRouter-hosted models (e.g., GPT-4o mini / Mistral)




📝 Mock Test Generator
Prelims & Mains mock paper generation
Difficulty control (Easy/Medium/Hard)
Current affairs integration
PYQ based test generation
Performance analytics


📰 Current Affairs Dashboard
Daily auto-updated news feed
Categorized by GS papers
Prelims vs Mains relevance tagging
Topic wise filtering
UPSC exam oriented classification

🛠 Tech Stack

Frontend-
React.js
Tailwind CSS
Lucide Icons
Recharts
Framer Motion


Backend-
FastAPI
Python
REST APIs
WebSocket Notifications


AI / ML-
OpenRouter (hosted LLMs)
Mistral / LLaMA / GPT-4o via OpenRouter
OpenAI API (Optional)
Sentence Transformers
RAG (Retrieval Augmented Generation)


Database & Storage-
Qdrant Vector DB
JSON based data store



System Architecture-
Frontend (React)
        |
        |
FastAPI Backend
        |
------------------------------
|             |              |
LLM Engine   Vector DB     Scheduler
(OpenRouter) (Qdrant)      (APScheduler)


📦 Installation Guide
1️⃣ Clone Repository
git clone https://github.com/your-username/upsc-scholar-ai.git
cd upsc-scholar-ai

2️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload

3️⃣ OpenRouter Setup (Hosted AI)
- Create an API key at https://openrouter.ai/keys
- Set env vars in backend/.env (or your shell):
        - OPENROUTER_API_KEY=sk-or-...
        - OPENROUTER_MODEL=openai/gpt-4o-mini (or your preferred model)
        - OPENROUTER_EMBED_MODEL=text-embedding-3-large
        - LLM_PROVIDER=openrouter

4️⃣ Frontend Setup
cd frontend
npm install
npm run dev

📂 Project Structure
upsc-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.py
│
├── frontend/
│   ├── src/
│   │   └── App.jsx
│
├── scripts/
│   ├── current_affairs/
│   └── pyq_data/
│
└── README.md



🤝 Contributing
Contributions are welcome!
Fork the repository
Create feature branch
Commit changes
Open Pull Request

📜 License
MIT License


👨‍💻 Developer
Swapna Kondapuram
BTech Student |SVNIT| Full Stack | AI/ML Developer

🔗 LinkedIn: https://www.linkedin.com/in/swapna-kondapuram-630626292/
🔗 GitHub: https://github.com/swap0506
⭐ Support

If you like this project:

🌟 Star this repo
🍴 Fork it
📢 Share with UPSC aspirants













