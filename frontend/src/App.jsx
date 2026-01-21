import React, { useState, useEffect } from "react";
import { Send, Bell, Brain, Clock, Award, TrendingUp, BookOpen, Trophy, ChevronLeft, ChevronRight, Home, Target, Mic, Newspaper, Upload, Moon, Sun, Mail, Phone, Book, Save, Plus, Trash2, LogOut, FileText, CheckCircle } from "lucide-react";

const App = () => {
  const [isAuth, setIsAuth] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [quote, setQuote] = useState({ text: 'Success comes to those who persevere.', author: 'Unknown' });

  useEffect(() => {

  const quotes = [
    { text: "Success is the sum of small efforts repeated daily.", author: "R. Collier" },
    { text: "Discipline is the bridge between goals and achievement.", author: "Jim Rohn" },
    { text: "Dream big. Start small. Act now.", author: "Robin Sharma" },
    { text: "The future depends on what you do today.", author: "Mahatma Gandhi" }
  ];

  const random = quotes[Math.floor(Math.random() * quotes.length)];
  setQuote(random);

}, []);


  const sidebarItems = [
    { id: "dashboard", label: "Dashboard", icon: Home },
    { id: "chat", label: "AI Assistant", icon: Brain },
    { id: "mock", label: "Mock Tests", icon: Target },
    { id: "notebook", label: "Notebook", icon: Book },
    { id: "evaluator", label: "Evaluator", icon: FileText },
    { id: "calendar", label: "Calendar", icon: BookOpen },
    { id: "affairs", label: "Current Affairs", icon: Newspaper },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard": return <Dashboard darkMode={darkMode} quote={quote} />;
      case "chat": return <ChatInterface darkMode={darkMode} />;
      case "mock": return <MockInterface darkMode={darkMode} />;
      case "notebook": return <NotebookInterface darkMode={darkMode} />;
      case "evaluator": return <EvaluatorInterface darkMode={darkMode} />;
      case "calendar": return <CalendarInterface darkMode={darkMode} />;
      case "affairs": return <AffairsInterface darkMode={darkMode} />;
      default: return <Dashboard darkMode={darkMode} quote={quote} />;
    }
  };

  if (!isAuth) {
    return (
      <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gradient-to-br from-blue-50 to-purple-50'} flex items-center justify-center p-4`}>
        <button onClick={() => setDarkMode(!darkMode)} className={`absolute top-6 right-6 p-3 ${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg`}>
          {darkMode ? <Sun className="w-6 h-6 text-yellow-400" /> : <Moon className="w-6 h-6" />}
        </button>
        <div className={`w-full max-w-md ${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-2xl p-8`}>
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Trophy className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">UPSC Mastery</h1>
          </div>
          <div className="space-y-4">
            <input type="email" placeholder="Email" className={`w-full px-4 py-3 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl outline-none`} />
            <input type="tel" placeholder="Phone (WhatsApp)" className={`w-full px-4 py-3 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl outline-none`} />
            <input type="password" placeholder="Password" className={`w-full px-4 py-3 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl outline-none`} />
            <button onClick={() => setIsAuth(true)} className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-bold">Login</button>
          </div>
          <div className={`mt-6 p-4 ${darkMode ? 'bg-gray-700' : 'bg-blue-50'} rounded-xl`}>
            <p className={`text-xs font-semibold ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Need Help?</p>
            <p className="text-xs text-blue-500">📞 6300708369</p>
            <p className="text-xs text-blue-500">✉️ swapnakondapuram05@gmail.com</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gradient-to-br from-blue-50 to-purple-50'}`}>
      <nav className={`${darkMode ? 'bg-gray-800' : 'bg-white'} border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'} sticky top-0 z-50`}>
        <div className="px-4 md:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <Trophy className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-lg md:text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">UPSC Mastery</h1>
          </div>
          <div className="flex gap-2 md:gap-4">
            <button onClick={() => setDarkMode(!darkMode)} className={`p-2 ${darkMode ? 'bg-gray-700' : 'bg-gray-50'} rounded-xl`}>
              {darkMode ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5" />}
            </button>
            <button onClick={() => setIsAuth(false)} className={`p-2 ${darkMode ? 'bg-gray-700' : 'bg-gray-50'} rounded-xl`}>
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </nav>

      <div className="flex">
        <aside className={`${sidebarCollapsed ? 'w-20' : 'w-64'} ${darkMode ? 'bg-gray-800' : 'bg-white'} border-r ${darkMode ? 'border-gray-700' : 'border-gray-200'} min-h-[calc(100vh-73px)] transition-all relative hidden md:block`}>
          <div className="p-4 space-y-2">
            {sidebarItems.map(item => {
              const Icon = item.icon;
              return (
                <button key={item.id} onClick={() => setActiveTab(item.id)} className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all hover:scale-105 ${activeTab === item.id ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg" : `${darkMode ? 'text-gray-300 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-100'}`}`}>
                  <Icon className="w-5 h-5" />
                  {!sidebarCollapsed && <span className="font-medium">{item.label}</span>}
                </button>
              );
            })}
          </div>
          {!sidebarCollapsed && (
            <div className={`absolute bottom-20 left-4 right-4 p-4 ${darkMode ? 'bg-gray-700' : 'bg-blue-50'} rounded-xl text-xs`}>
              <p className="font-semibold mb-2">Contact Support</p>
              <p className="text-blue-500">📞 6300708369</p>
              <p className="text-blue-500 break-all">✉️ swapnakondapuram05@gmail.com</p>
            </div>
          )}
          <button onClick={() => setSidebarCollapsed(!sidebarCollapsed)} className={`absolute -right-3 top-8 w-6 h-6 ${darkMode ? 'bg-gray-800' : 'bg-white'} border-2 rounded-full flex items-center justify-center`}>
            {sidebarCollapsed ? <ChevronRight className="w-3 h-3" /> : <ChevronLeft className="w-3 h-3" />}
          </button>
        </aside>

        {/* Mobile Bottom Navigation */}
        <nav className={`md:hidden fixed bottom-0 left-0 right-0 ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-t z-50`}>
          <div className="flex justify-around items-center p-2">
            {sidebarItems.map(item => {
              const Icon = item.icon;
              return (
                <button key={item.id} onClick={() => setActiveTab(item.id)} className={`flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-all ${activeTab === item.id ? "text-blue-500" : `${darkMode ? 'text-gray-400' : 'text-gray-600'}`}`}>
                  <Icon className="w-5 h-5" />
                  <span className="text-xs">{item.label}</span>
                </button>
              );
            })}
          </div>
        </nav>

        <main className="flex-1 p-4 md:p-6 w-full overflow-x-hidden pb-20 md:pb-6">{renderContent()}</main>
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




const ChatInterface = ({ darkMode }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setInput("");
    setMessages([...messages, { type: 'user', text: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, session_id: "123", use_gpt4: false })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { type: 'ai', text: data.response }]);
    } catch {
      setMessages(prev => [...prev, { type: 'ai', text: '⚠️ Backend unavailable' }]);
    }
    setLoading(false);
  };

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-lg h-[calc(100vh-170px)] flex flex-col max-w-full`}>
      <div className={`p-4 md:p-6 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <h2 className={`text-lg md:text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>AI Study Assistant</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] md:max-w-[80%] px-3 md:px-4 py-2 md:py-3 rounded-2xl text-sm md:text-base ${msg.type === 'user' ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white' : `${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-800'}`}`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <div className={`p-4 md:p-6 border-t ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="flex gap-2 md:gap-3">
          <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendMessage()} placeholder="Ask anything..." className={`flex-1 px-3 md:px-4 py-2 md:py-3 text-sm md:text-base ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} rounded-xl outline-none`} />
          <button onClick={sendMessage} disabled={loading} className="px-4 md:px-6 py-2 md:py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl disabled:opacity-50"><Send className="w-4 h-4 md:w-5 md:h-5" /></button>
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

          if (prev <= 1) {
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

      <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white"} p-6 rounded-xl shadow-xl max-w-4xl mx-auto`}>

        <h2 className="text-2xl font-bold mb-6">
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
                className={`p-3 rounded-xl font-semibold capitalize
                ${config.examType === t
                  ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white"
                  : darkMode ? "bg-gray-700" : "bg-gray-100"}`}
              >
                {t}
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
                className={`p-3 rounded-xl text-left
                ${config.paperType === p.id
                  ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white"
                  : darkMode ? "bg-gray-700" : "bg-gray-100"}`}
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
              className="w-12 h-12 bg-gray-200 rounded-xl font-bold"
            >
              −
            </button>

            <div className="text-xl font-bold">
              {config.numQuestions}
            </div>

            <button
              onClick={() =>
                setConfig({ ...config, numQuestions: Math.min(maxQ, config.numQuestions + 5) })}
              className="w-12 h-12 bg-gray-200 rounded-xl font-bold"
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
                className={`p-3 rounded-xl capitalize
                ${config.difficulty === d
                  ? "bg-gradient-to-r from-green-500 to-blue-500 text-white"
                  : darkMode ? "bg-gray-700" : "bg-gray-100"}`}
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
            checked={config.currentAffairs}
            onChange={e =>
              setConfig({ ...config, currentAffairs: e.target.checked })}
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

    const q = test.questions[current];

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
              onClick={handleSubmit}
              className="px-6 py-2 bg-red-500 text-white rounded"
            >
              Submit Test
            </button>

            <button
              disabled={current === test.questions.length - 1}
              onClick={() => setCurrent(current + 1)}
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

const EvaluatorInterface = ({ darkMode }) => {
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState('');

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-lg p-8 max-w-4xl mx-auto`}>
      <h2 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'} mb-6`}>Answer Evaluator</h2>
      <textarea value={question} onChange={e => setQuestion(e.target.value)} placeholder="Question..." rows="3" className={`w-full px-4 py-3 mb-4 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl`} />
      <div className={`border-2 border-dashed ${darkMode ? 'border-gray-600' : 'border-gray-300'} rounded-xl p-8 text-center mb-4`}>
        <input type="file" id="upload" multiple accept=".pdf,image/*" onChange={e => setFiles([...files, ...Array.from(e.target.files)])} className="hidden" />
        <label htmlFor="upload" className="cursor-pointer">
          <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
          <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Upload PDF/Images</p>
        </label>
      </div>
      <button className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-bold">Evaluate</button>
    </div>
  );
};

const CalendarInterface = ({ darkMode }) => {
  const [events, setEvents] = useState([]);
  const [event, setEvent] = useState({ title: '', date: '' });

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-lg p-8 max-w-2xl mx-auto`}>
      <h2 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'} mb-6`}>Calendar</h2>
      <div className="grid grid-cols-2 gap-4 mb-4">
        <input value={event.title} onChange={e => setEvent({...event, title: e.target.value})} placeholder="Event..." className={`px-4 py-3 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl`} />
        <input type="date" value={event.date} onChange={e => setEvent({...event, date: e.target.value})} className={`px-4 py-3 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'} border rounded-xl`} />
      </div>
      <button onClick={() => { if(event.title && event.date) { setEvents([...events, {...event, id: Date.now()}]); setEvent({title:'', date:''}); }}} className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl mb-6"><Plus className="w-5 h-5 inline mr-2" />Add</button>
      <div className="space-y-3">
        {events.map(e => (
          <div key={e.id} className={`p-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-50'} rounded-xl`}>
            <h4 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>{e.title}</h4>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>{e.date}</p>
          </div>
        ))}
      </div>
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






export default App;