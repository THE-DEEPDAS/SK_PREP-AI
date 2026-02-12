import React, { useState, useEffect } from "react";
import { Send } from "lucide-react";
import {
  Bell, Brain, Clock, Award, TrendingUp, BookOpen, Trophy,
  ChevronLeft, ChevronRight,Upload, Home, Target, Newspaper,
  Moon, Sun, Phone, Mail, LogOut, FileText, Book
} from "lucide-react";

const DashboardApp = () => {

  const [darkMode, setDarkMode] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [quote, setQuote] = useState({
    text: "Success comes to those who persevere.",
    author: "Unknown"
  });
  useEffect(() => {

  const fetchQuote = async () => {
    try {

      const res = await fetch("https://dummyjson.com/quotes/random");

      if (!res.ok) throw new Error("API Error");

      const data = await res.json();

      setQuote({
        text: data.quote,
        author: data.author
      });

    } catch (error) {

      console.error("Quote fetch failed:", error);

      setQuote({
        text: "The future depends on what you do today.",
        author: "Mahatma Gandhi"
      });

    }
  };

  fetchQuote();

}, []);

  // ✅ LOGOUT HANDLER
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  const sidebarItems = [
    { id: "dashboard", label: "Dashboard", icon: Home },
    { id: "chat", label: "AI Assistant", icon: Brain },
    { id: "mock", label: "Mock Tests", icon: Target },
    { id: "notebook", label: "Notebook", icon: Book },
    { id: "evaluator", label: "Evaluator", icon: FileText },
    // { id: "calendar", label: "Calendar", icon: BookOpen },
    { id: "affairs", label: "Current Affairs", icon: Newspaper },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard": return <Dashboard darkMode={darkMode} quote={quote} />;
      case "chat": return <ChatInterface darkMode={darkMode} />;
      case "mock": return <MockInterface darkMode={darkMode} />;
      case "notebook": return <NotebookInterface darkMode={darkMode} />;
      case "evaluator": return <EvaluatorInterface darkMode={darkMode} />;
      // case "calendar": return <CalendarInterface darkMode={darkMode} />;
      case "affairs": return <AffairsInterface darkMode={darkMode} />;
      default: return <Dashboard darkMode={darkMode} quote={quote} />;
    }
  };

  // ================= DASHBOARD UI =================

  return (
    <div className={`min-h-screen ${darkMode ? "bg-gray-900" : "bg-gray-50"}`}>

      {/* TOP BAR */}
      <div className={`${darkMode ? "bg-gray-800" : "bg-white"} border-b sticky top-0 z-40`}>
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">

          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
              <Trophy className="text-white" />
            </div>
            <h1 className={`${darkMode ? "text-white" : "text-gray-800"} font-bold text-xl`}>
              UPSC Mastery
            </h1>
          </div>

          <div className="flex gap-3">

            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-xl bg-gray-100"
            >
              {darkMode ? <Sun /> : <Moon />}
            </button>

            {/* ✅ LOGOUT */}
            <button
              onClick={handleLogout}
              className="p-2 rounded-xl bg-gray-100"
            >
              <LogOut />
            </button>

          </div>
        </div>
      </div>

      <div className="flex">

        {/* SIDEBAR */}
        <div className={`${sidebarCollapsed ? "w-20" : "w-64"} ${darkMode ? "bg-gray-800" : "bg-white"} border-r hidden md:block`}>

          <div className="p-4 space-y-2">
            {sidebarItems.map(item => {
              const Icon = item.icon;

              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl
                  ${activeTab === item.id
                      ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white"
                      : darkMode ? "text-gray-300 hover:bg-gray-700" : "text-gray-700 hover:bg-gray-100"
                    }`}
                >
                  <Icon size={18} />
                  {!sidebarCollapsed && item.label}
                </button>
              );
            })}
          </div>

          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="absolute -right-3 top-10 bg-white border rounded-full p-1"
          >
            {sidebarCollapsed ? <ChevronRight /> : <ChevronLeft />}
          </button>

        </div>

        {/* MAIN CONTENT */}
        <div className="flex-1 min-h-[600px]">
          {renderContent()}
        </div>

      </div>
    </div>
  );
};


const Dashboard = ({ darkMode, quote }) => {

  const [stats, setStats] = useState([
    { label: 'Articles Today', value: '0', icon: Clock, color: 'from-blue-400 to-blue-600', change: '--' },
    { label: 'Categories Covered', value: '0', icon: Target, color: 'from-teal-400 to-teal-600', change: '--' },
    { label: 'News Sources', value: '0', icon: Award, color: 'from-purple-400 to-purple-600', change: '--' },
    { label: 'Coverage Score', value: '0%', icon: TrendingUp, color: 'from-pink-400 to-pink-600', change: '--' }
  ]);

  const [loading, setLoading] = useState(true);

  // ================= FETCH STATS =================

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/current-affairs/stats"
      );

      if (!response.ok) {
        throw new Error("Stats API Failed");
      }

      const data = await response.json();

      const totalArticles = data?.total_articles ?? 0;
      const categories = Object.keys(data?.category_distribution || {}).length;
      const sources = Object.keys(data?.source_distribution || {}).length;

      setStats([
        {
          label: "Articles Today",
          value: totalArticles,
          icon: Clock,
          color: "from-blue-400 to-blue-600",
          change: "+Live"
        },
        {
          label: "Categories Covered",
          value: categories,
          icon: Target,
          color: "from-teal-400 to-teal-600",
          change: "+Auto"
        },
        {
          label: "News Sources",
          value: sources,
          icon: Award,
          color: "from-purple-400 to-purple-600",
          change: "+Active"
        },
        {
          label: "Coverage Score",
          value: totalArticles > 0 ? "100%" : "0%",
          icon: TrendingUp,
          color: "from-pink-400 to-pink-600",
          change: "+Updated"
        }
      ]);

    } catch (error) {

      console.warn("Dashboard Offline Mode");

      // fallback UI (backend down)
      setStats([
        { label: "Articles Today", value: "--", icon: Clock, color: "from-blue-400 to-blue-600", change: "--" },
        { label: "Categories Covered", value: "--", icon: Target, color: "from-teal-400 to-teal-600", change: "--" },
        { label: "News Sources", value: "--", icon: Award, color: "from-purple-400 to-purple-600", change: "--" },
        { label: "Coverage Score", value: "--", icon: TrendingUp, color: "from-pink-400 to-pink-600", change: "--" }
      ]);

    }

    setLoading(false);
  };

  // ================= UI =================

  return (

    <div className="space-y-6 max-w-7xl mx-auto">

      {/* Quote Card */}
      <div className={`${darkMode ? "bg-gray-800" : "bg-white"} rounded-2xl shadow-lg p-5`}>
        <p className={`italic text-lg ${darkMode ? "text-gray-200" : "text-gray-800"}`}>
          "{quote?.text || "Stay consistent. Success will follow."}"
        </p>
        <p className={`text-sm mt-2 ${darkMode ? "text-gray-400" : "text-gray-600"}`}>
          — {quote?.author || "UPSC Mentor"}
        </p>
      </div>


      {/* Loader */}
      {loading ? (

        <div className="flex justify-center py-20">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>

      ) : (

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

          {stats.map((stat, idx) => {

            const Icon = stat.icon;

            return (

              <div
                key={idx}
                className={`${darkMode ? "bg-gray-800" : "bg-white"} 
                rounded-2xl shadow-lg p-5 transition-all 
                hover:shadow-xl hover:-translate-y-1 cursor-pointer`}
              >

                <div className="flex justify-between mb-4">

                  <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} 
                  rounded-xl flex items-center justify-center`}>
                    <Icon className="text-white" />
                  </div>

                  <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-lg font-semibold">
                    {stat.change}
                  </span>

                </div>

                <div className={`text-3xl font-bold ${darkMode ? "text-white" : "text-gray-800"}`}>
                  {stat.value}
                </div>

                <div className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-600"}`}>
                  {stat.label}
                </div>

              </div>
            );
          })}

        </div>
      )}

    </div>
  );
};




const ChatInterface = ({ darkMode=false }) => {

  const [messages, setMessages] = useState([
    { type: 'ai', text: 'Hello 👋 Ask me anything about UPSC preparation.' }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!input.trim()) return;

    const userMsg = input;
    setInput("");

    setMessages(prev => [...prev, { type: 'user', text: userMsg }]);
    setLoading(true);

    try {

      const res = await fetch('http://127.0.0.1:8000/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMsg,
          session_id: "123",
          use_gpt4: false
        })
      });

      const data = await res.json();

      setMessages(prev => [...prev, {
        type: 'ai',
        text: data.response || data.message || "No reply received"
      }]);

    } catch (err) {

      console.error(err);

      setMessages(prev => [...prev, {
        type: 'ai',
        text: '⚠️ Backend unavailable'
      }]);

    }

    setLoading(false);
  };

  return (

    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-lg min-h-[500px] h-full flex flex-col w-full`}>

      <div className={`p-4 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <h2 className={`text-lg font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
          AI Study Assistant
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">

        {Array.isArray(messages) && messages?.length >0 && messages.map((msg, i) => (

          <div key={i} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>

            <div className={`max-w-[80%] px-4 py-2 rounded-2xl text-sm
              ${msg.type === 'user'
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                : darkMode
                  ? 'bg-gray-700 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}>

              {msg.text}

            </div>

          </div>

        ))}

      </div>

      <div className={`p-4 border-t ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>

        <div className="flex gap-3">

          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
            placeholder="Ask anything..."
            className={`flex-1 px-4 py-2 text-sm rounded-xl outline-none
            ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
            className="px-5 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl disabled:opacity-50"
          >
            Send 
          </button>

        </div>

      </div>

    </div>
  );
};




 




const MockInterface = ({ darkMode }) => {

  // ================= STATES =================

  const [stage, setStage] = useState("config");

  const [config, setConfig] = useState({
    examType: "prelims",
    paperType: "gs1",
    numQuestions: 10,
    difficulty: "medium",
    questionSource: "mock",
    currentAffairs: false
  });

  const [test, setTest] = useState(null);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);


  // ================= PAPER OPTIONS =================

  const paperOptions = {

    prelims: [
      {
        id: "gs1",
        name: "GS Paper I",
        desc: "History, Polity, Geography, Economy"
      }
    ],

    mains: [
      { id: "gs1", name: "GS Paper 1", desc: "Culture, History, Geography" },
      { id: "gs2", name: "GS Paper 2", desc: "Polity, Governance, IR" },
      { id: "gs3", name: "GS Paper 3", desc: "Economy, Tech, Environment" },
      { id: "gs4", name: "GS Paper 4", desc: "Ethics, Integrity" }
    ]
  };


  // ================= TIMER =================

  useEffect(() => {

    if (stage === "test" && timeRemaining > 0) {

      const timer = setInterval(() => {

        setTimeRemaining(prev => {

          if (prev == 1) {
            clearInterval(timer);
            handleSubmit();
            return 0;
          }

          return prev - 1;
        });

      }, 1000);

      return () => clearInterval(timer);
    }

  }, [stage, timeRemaining]);


  // ================= TIME FORMAT =================

  const formatTime = (seconds) => {

    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;

    return `${mins.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };


  // ================= GENERATE TEST =================

  const generate = async () => {

    setLoading(true);

    try {

      const res = await fetch("http://127.0.0.1:8000/api/mock/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },

        body: JSON.stringify({
          exam_type: config.examType,
          paper_type: config.paperType,
          num_questions: config.numQuestions,
          difficulty: config.difficulty,
          question_source: config.questionSource,
          include_current_affairs: config.currentAffairs
        })
      });

      if (!res.ok) throw new Error("Generation failed");

      const data = await res.json();

      setTest(data);
      setTimeRemaining(data.duration_minutes * 60);
      setAnswers({});
      setCurrent(0);
      setStage("test");

    } catch (err) {

      alert("Generation Error");

    }

    setLoading(false);
  };


  // ================= SUBMIT TEST =================

  const handleSubmit = async () => {

    if (!window.confirm("Submit Test?")) return;

    setLoading(true);

    try {

      const res = await fetch(
        `http://127.0.0.1:8000/api/mock/submit/${test.test_id}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ answers })
        }
      );

      const data = await res.json();

      setResults(data);
      setStage("result");

    } catch (err) {

      alert("Submit Failed");

    }

    setLoading(false);
  };


  // ================= CONFIG SCREEN =================

  if (stage === "config") {

    const maxQ = config.examType === "prelims" ? 100 : 25;

    return (

      <div className={`${darkMode 
        ? "bg-gradient-to-br from-slate-800 via-slate-900 to-slate-800 text-white border border-slate-700" 
        : "bg-white text-gray-900 border border-gray-200"} 
        p-8 rounded-2xl shadow-2xl max-w-4xl mx-auto`}>

        <h2 className={`text-3xl font-extrabold mb-6 tracking-wide
        ${darkMode ? "text-white" : "text-gray-900"}`}>
          Mock Test Generator
        </h2>


        {/* EXAM TYPE */}
        <div className="mb-6">

          <label className="font-semibold mb-2 block">Exam Type</label>

          <div className="grid grid-cols-2 gap-4">

            {["prelims", "mains"].map(t => (

              <button
                key={t}
                onClick={() =>
                  setConfig({
                    ...config,
                    examType: t,
                    paperType: paperOptions[t][0].id
                  })}
                  className={`p-3 rounded-xl font-semibold capitalize transition
                    ${config.examType === t
                      ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white"
                      : darkMode
                        ? "bg-gray-700 text-white border border-gray-600"
                        : "bg-white text-gray-800 border border-gray-300 shadow-sm"
}`}>

              <div className="font-bold">{t}</div>

            </button>

          ))}

        </div>

      </div>


        {/* PAPER */}
        <div className="mb-6">

          <label className="font-semibold mb-2 block">Paper</label>

          <div className="grid grid-cols-2 gap-4">

            {paperOptions[config.examType].map(p => (

              <button
                key={p.id}
                onClick={() => setConfig({ ...config, paperType: p.id })}
                className={`p-3 rounded-xl text-left transition
                  ${config.paperType === p.id
                    ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white"
                    : darkMode
                      ? "bg-gray-700 text-white border border-gray-600"
                      : "bg-white text-gray-800 border border-gray-300 shadow"
     }`}
              >
                <div className="font-bold">{p.name}</div>
                <div className="text-sm opacity-70">{p.desc}</div>
              </button>

            ))}

          </div>

        </div>


        {/* QUESTIONS COUNT */}
        <div className="mb-6">

          <label className="font-semibold mb-2 block">Questions</label>

          <div className="flex items-center gap-4">

            <button
              onClick={() =>
                setConfig({ ...config, numQuestions: Math.max(1, config.numQuestions - 5) })}
              className={`w-12 h-12 rounded-xl font-bold border
                ${darkMode
                  ? "bg-gray-700 text-white border-gray-600"
                  : "bg-white text-gray-800 border-gray-300 shadow"
                }`}
            >
              −
            </button>

            <div className="text-xl font-bold">
              {config.numQuestions}
            </div>

            <button
              onClick={() =>
                setConfig({ ...config, numQuestions: Math.min(maxQ, config.numQuestions + 5) })}
                className={`w-12 h-12 rounded-xl font-bold border
                ${darkMode
                  ? "bg-gray-700 text-white border-gray-600"
                  : "bg-white text-gray-800 border-gray-300 shadow"
                }`}
            >
              +
            </button>

          </div>

        </div>


        {/* DIFFICULTY */}
        <div className="mb-6">

          <label className="font-semibold mb-2 block">Difficulty</label>

          <div className="grid grid-cols-3 gap-3">

            {["easy", "medium", "hard"].map(d => (

              <button
                key={d}
                onClick={() => setConfig({ ...config, difficulty: d })}
                className={`p-3 rounded-xl capitalize transition
                  ${config.difficulty === d
                    ? "bg-gradient-to-r from-green-500 to-blue-500 text-white"
                    : darkMode
                      ? "bg-gray-700 text-white border border-gray-600"
                      : "bg-white text-gray-800 border border-gray-300 shadow-sm"
}`}
              >
                {d}
              </button>

            ))}

          </div>

        </div>


        {/* CURRENT AFFAIRS */}
        <div className="mb-6 flex items-center gap-3">

          <input
            type="checkbox"
            className="w-5 h-5 accent-blue-600"
            checked={config.currentAffairs}
            onChange={e =>
              setConfig({ ...config, currentAffairs: e.target.checked })
            }
          />

          <span>Include Current Affairs</span>

        </div>


        {/* GENERATE BUTTON */}
        <button
          onClick={generate}
          disabled={loading}
          className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-bold"
        >
          {loading ? "Generating..." : "Generate Test"}
        </button>

      </div>
    );
  }


  // ================= TEST SCREEN =================

  if (stage === "test" && test) {

    const q = test.questions[current] || null;
    if(!q) {
      handleSubmit();
      return null;
    }

    return (

      <div className="max-w-5xl mx-auto p-6">

        <div className="flex justify-between mb-4">

          <div className="font-bold">
            Question {current + 1}/{test.questions.length}
          </div>

          <div className="font-bold text-blue-600">
            {formatTime(timeRemaining)}
          </div>

        </div>


        <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white"} p-6 rounded-xl shadow`}>

          <p className="text-lg font-semibold mb-5">
            {q.question}
          </p>


          {q.options.map((opt, idx) => {

            const selected = answers[q.id] === opt;

            return (

              <div
                key={idx}
                onClick={() =>
                  setAnswers({ ...answers, [q.id]: opt })}
                className={`p-3 mb-3 border rounded cursor-pointer
                ${selected
                  ? "bg-blue-500 text-white border-blue-500"
                  : darkMode
                    ? "border-gray-600 hover:bg-gray-700"
                    : "border-gray-300 hover:bg-gray-100"}`}
              >
                {opt}
              </div>

            );
          })}


          <div className="flex justify-between mt-6">

            <button
              disabled={current === 0}
              onClick={() => setCurrent(current - 1)}
              className="px-4 py-2 bg-gray-200 rounded"
            >
              Prev
            </button>

            <button
              disabled={loading}
              onClick={()=>{
                if(!loading) handleSubmit();
              }}
              className="px-6 py-2 bg-red-500 text-white rounded"
            >
              Submit Test
            </button>

            <button
              disabled={current === test.questions.length - 1}
              onClick={() => {
                if (current < test.questions.length - 1) {
                  setCurrent(current + 1);
                }
              }}
              className="px-4 py-2 bg-gray-200 rounded"
            >
              Next
            </button>

          </div>

        </div>

      </div>
    );
  }


  // ================= RESULT =================

  if (stage === "result" && results) {

    return (

      <div className="max-w-3xl mx-auto p-6 text-center">

        <h2 className="text-3xl font-bold mb-4">
          Test Result
        </h2>

        <p className="text-xl">
          Score: {results.score} / {results.total}
        </p>

        <button
          onClick={() => setStage("config")}
          className="mt-6 px-6 py-3 bg-blue-500 text-white rounded-xl"
        >
          New Test
        </button>

      </div>
    );
  }

};








const NotebookInterface = ({ darkMode }) => {
  const [notes, setNotes] = useState([]);
  const [note, setNote] = useState({ title: '', content: '' });

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-lg p-8 max-w-4xl mx-auto`}>
      <h2 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'} mb-6`}>Notebook</h2>
      <input value={note.title} onChange={e => setNote({...note, title: e.target.value})} placeholder="Title..." className={`w-full px-4 py-3 mb-4 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl`} />
      <textarea value={note.content} onChange={e => setNote({...note, content: e.target.value})} placeholder="Notes..." rows="10" className={`w-full px-4 py-3 mb-4 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl resize-none`} />
      <button onClick={() => { if(note.title && note.content) { setNotes([...notes, {...note, id: Date.now()}]); setNote({title:'', content:''}); }}} className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl"><Save className="w-5 h-5 inline mr-2" />Save</button>
    </div>
  );
};






const EvaluatorInterface = () => {

  const [language, setLanguage] = useState("English");
  const [paper, setPaper] = useState("");
  const [marks, setMarks] = useState(10);
  const [difficulty, setDifficulty] = useState("hard");

  const [question, setQuestion] = useState("");
  const [files, setFiles] = useState([]);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // ================= FILE =================

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  // ================= API =================
  
  const handleEvaluate = async () => {

  if (!paper) return alert("Select Paper");
  if (!files.length) return alert("Upload Answer");

  setLoading(true);
  setError(null);

  try {

    const formData = new FormData();

    files.forEach(f => formData.append("files", f));

    formData.append("paper", paper);
    formData.append("marks", String(marks)); // ✅ FIX
    formData.append("difficulty", difficulty);
    formData.append("question", question || ""); // ✅ FIX

    const res = await fetch(
      "http://127.0.0.1:8000/api/evaluator/evaluate-upload",
      {
        method: "POST",
        body: formData
      }
    );

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Evaluation Failed");

    setResult(data);

  } catch (err) {
    setError(err.message);
  }

  setLoading(false);
};

  return (

    <div className="bg-[#f5f7fb] min-h-screen p-6">

      <h1 className="text-2xl font-bold text-gray-900 mb-6">
        Mains Evaluator
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* LEFT */}

        <div className="lg:col-span-2 space-y-5">

          {/* PAPER */}

          <div className="bg-white p-5 rounded-xl shadow">

            <h3 className="font-semibold text-gray-800 mb-3">
              Paper Type & Language
            </h3>

            <div className="flex gap-3 mb-3">

              <button
                onClick={() => setLanguage("English")}
                className={`px-4 py-2 rounded-full border font-medium
                ${language === "English"
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-800"
                }`}
              >
                English
              </button>

              <button
                onClick={() => setLanguage("Hindi")}
                className={`px-4 py-2 rounded-full border font-medium
                ${language === "Hindi"
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-800"
                }`}
              >
                हिंदी
              </button>

            </div>

            <select
              value={paper}
              onChange={(e) => setPaper(e.target.value)}
              className="w-full border p-3 rounded-lg text-gray-800 bg-gray-50"
            >
              <option value="">Select Paper</option>
              <option>GS Paper I</option>
              <option>GS Paper II</option>
              <option>GS Paper III</option>
              <option>GS Paper IV</option>
              <option>Essay</option>
            </select>

          </div>

          {/* MARKS */}

          <div className="bg-white p-5 rounded-xl shadow">

            <h3 className="font-semibold text-gray-800 mb-3">
              Question Marks
            </h3>

            <div className="grid grid-cols-3 gap-4">

              {[10, 15, 20].map(m => (

                <button
                  key={m}
                  onClick={() => setMarks(m)}
                  className={`py-3 rounded-lg border font-bold
                  ${marks === m
                      ? "bg-green-500 text-white shadow"
                      : "bg-white text-gray-800"
                  }`}
                >
                  {m} Marks
                </button>

              ))}

            </div>

          </div>

          {/* MODE */}

          <div className="bg-white p-5 rounded-xl shadow">

            <h3 className="font-semibold text-gray-800 mb-3">
              Evaluator Mode
            </h3>

            <div className="grid grid-cols-2 gap-4">

              <button
                onClick={() => setDifficulty("hard")}
                className={`py-3 rounded-lg border font-bold
                ${difficulty === "hard"
                    ? "bg-red-500 text-white"
                    : "bg-white text-gray-800"
                }`}
              >
                Hard
              </button>

              <button
                onClick={() => setDifficulty("easy")}
                className={`py-3 rounded-lg border font-bold
                ${difficulty === "easy"
                    ? "bg-green-500 text-white"
                    : "bg-white text-gray-800"
                }`}
              >
                Easy
              </button>

            </div>

          </div>

          {/* QUESTION */}

          <div className="bg-white p-5 rounded-xl shadow">

            <textarea
              placeholder="Enter question..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="w-full p-3 border rounded-lg bg-gray-50 text-gray-800"
            />

          </div>

          {/* UPLOAD */}

          <div className="bg-white p-5 rounded-xl shadow">

            <label className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center cursor-pointer">

              <Upload className="text-gray-500 mb-2" size={40} />

              <span className="text-gray-700">
                Upload PDF / JPG / PNG
              </span>

              <input
                type="file"
                multiple
                hidden
                onChange={handleFileChange}
              />

            </label>

            {files.map((f, i) => (
              <p key={i} className="text-sm mt-2 text-gray-700">
                📄 {f.name}
              </p>
            ))}

          </div>

          {/* BUTTON */}

          <button
            onClick={handleEvaluate}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-bold shadow hover:bg-blue-700"
          >
            {loading ? "Evaluating..." : "Evaluate Answer"}
          </button>

          {error && (
            <p className="text-red-600">{error}</p>
          )}

        </div>

        {/* RIGHT PANEL */}

        <div className="bg-white p-5 rounded-xl shadow h-fit">

          <h3 className="font-semibold text-gray-800 mb-2">
            Current Selection
          </h3>

          <p className="text-gray-700">Marks: {marks}</p>
          <p className="text-gray-700">Mode: {difficulty}</p>
          <p className="text-gray-700">Language: {language}</p>

        </div>

      </div>

      {/* RESULT */}

      {result && (

        <div className="bg-white mt-8 p-6 rounded-xl shadow">

          <h2 className="font-bold text-xl text-gray-800 mb-2">
            Result
          </h2>

          <p className="text-lg text-blue-600 font-bold">
            Score: {result.final_score}/{marks}
          </p>

        </div>

      )}

    </div>
  );
};

const API = "http://127.0.0.1:8000/api/current-affairs/articles";

const prelimsCats = [
  "Polity",
  "Economy",
  "Environment",
  "Science",
  "History",
  "Geography"
];

const mainsCats = [
  "GS1",
  "GS2",
  "GS3",
  "GS4"
];

const AffairsInterface = ({ darkMode }) => {

  // ================= STATE =================

  const [examType, setExamType] = useState("prelims");
  const [category, setCategory] = useState("");
  const [date, setDate] = useState(
    new Date().toISOString().split("T")[0]
  );

  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);


  // ================= FETCH =================

  const fetchArticles = async () => {

    try {

      setLoading(true);

      const url =
        `${API}?date=${date}&exam_type=${examType}&categories=${category}`;

      const res = await fetch(url);
      const data = await res.json();

      let list = data?.articles || [];

      // REMOVE DUPLICATES BY TITLE
      const seen = new Set();
      list = list.filter(a => {
        if (!a.title) return false;
        if (seen.has(a.title)) return false;
        seen.add(a.title);
        return true;
      });

      setArticles(list);

    } catch (err) {

      console.error("Fetch failed:", err);
      setArticles([]);

    } finally {

      setLoading(false);

    }
  };


  // ================= EFFECT =================

  useEffect(() => {
    fetchArticles();
  }, [examType, category, date]);


  // ================= UI =================

  return (

    <div className="max-w-7xl mx-auto p-6 space-y-6">


      {/* HEADER */}
      <h2 className={`text-3xl font-bold ${darkMode ? "text-white" : "text-gray-800"}`}>
        Current Affairs
      </h2>


      {/* DATE PICKER */}
      <div className="flex justify-center">

        <input
          type="date"
          value={date}
          onChange={e => setDate(e.target.value)}
          className="px-4 py-2 rounded-xl shadow border bg-black text-white"
        />

      </div>


      {/* PRELIMS / MAINS SWITCH */}
      <div className="flex justify-center gap-4">

        {["prelims", "mains"].map(t => (

          <button
            key={t}
            onClick={() => {
              setExamType(t);
              setCategory("");
            }}

            className={`px-6 py-2 rounded-xl font-semibold transition
            ${examType === t
              ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            {t.toUpperCase()}
          </button>

        ))}

      </div>


      {/* CATEGORY FILTERS */}
      <div className="flex flex-wrap justify-center gap-3">

        {(examType === "prelims" ? prelimsCats : mainsCats).map(c => (

          <button
            key={c}
            onClick={() => setCategory(c)}

            className={`px-4 py-2 rounded-lg border font-medium
            ${category === c
              ? "bg-blue-500 text-white shadow"
              : "bg-white text-gray-700 hover:bg-blue-50"
            }`}
          >
            {c}
          </button>

        ))}

      </div>


      {/* LOADING */}
      {loading && (

        <div className="text-center text-gray-400 mt-10">
          Loading current affairs...
        </div>

      )}


      {/* EMPTY */}
      {!loading && articles.length === 0 && (

        <div className="text-center text-gray-400 mt-10">
          No articles available for selected date
        </div>

      )}


      {/* ARTICLES GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {articles.map((a, i) => (

          <div
            key={i}
            onClick={() => a.url && window.open(a.url, "_blank")}

            className={`p-6 rounded-2xl shadow transition cursor-pointer
            hover:-translate-y-1 hover:shadow-xl
            ${darkMode ? "bg-gray-800" : "bg-white"}`}
          >

            {/* TAGS */}
            <div className="flex gap-2 mb-3">

              <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs">

                {typeof a.category === "string" ? a.category : "General"}

              </span>

              <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-xs">

                {examType === "prelims" ? "Prelims" : "Mains"}

              </span>

            </div>


            {/* TITLE */}
            <h3 className={`font-bold text-lg mb-2
              ${darkMode ? "text-white" : "text-gray-800"}`}
            >
              {a.title || "Untitled Article"}
            </h3>


            {/* SUMMARY */}
            <p className={`text-sm mb-4
              ${darkMode ? "text-gray-400" : "text-gray-600"}`}
            >

              {typeof a.summary === "string" && a.summary.length > 20
                ? a.summary.slice(0, 220) + "..."
                : "Click to read full article"}

            </p>


            {/* FOOTER */}
            <div className="flex justify-between text-xs text-gray-400">

              <span>
                {typeof a.date === "string"
                  ? a.date.slice(0, 10)
                  : ""}
              </span>

              <span>
                {typeof a.source === "string"
                  ? a.source
                  : "News"}
              </span>

            </div>

          </div>

        ))}

      </div>

    </div>

  );
};






export default DashboardApp;