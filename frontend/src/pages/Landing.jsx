
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import SEO from "../components/SEO";
import { motion } from "framer-motion";

import heroImg from "../assets/online-learning.png";
import learnImg from "../assets/ai-research.png";


export default function About() {

  return (
    <div>

      <SEO
        title="About UPSC Mastery | AI Powered UPSC Platform"
        description="Learn how UPSC Mastery uses AI to transform IAS preparation with smart tools and automation."
      />

      <Navbar />

      {/* ================= HERO SECTION ================= */}
      <section className="relative bg-gradient-to-br from-slate-900 via-indigo-900 to-purple-900 py-28 overflow-hidden">

        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-32 left-20 w-96 h-96 bg-indigo-500/20 rounded-full blur-[120px] animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-[28rem] h-[28rem] bg-purple-500/20 rounded-full blur-[140px] animate-pulse delay-1000"></div>
        </div>

        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-14 items-center px-6 relative z-10">

          {/* LEFT */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >

            <div className="inline-flex mb-5 px-4 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-full text-white text-sm">
              🚀 AI Powered Learning Platform
            </div>

            <h1 className="text-5xl md:text-6xl font-extrabold mb-6 text-white">
              Revolutionizing
              <span className="block bg-gradient-to-r from-yellow-300 to-amber-400 bg-clip-text text-transparent">
                UPSC Preparation
              </span>
            </h1>

            <p className="text-white/80 text-lg mb-8 max-w-xl">
              Intelligent preparation companion that adapts to your pace and helps you crack India's toughest exam.
            </p>

            <div className="flex gap-4">
              <button className="px-8 py-4 bg-indigo-600 text-white rounded-full font-semibold">
                Start Your Journey
              </button>
              <button className="px-8 py-4 border border-white/30 text-white rounded-full">
                Watch Demo
              </button>
            </div>

          </motion.div>

          {/* RIGHT */}
          <motion.div className="flex justify-center">
            <img src={heroImg} alt="AI Learning" className="max-w-md drop-shadow-2xl" />
          </motion.div>

        </div>

      </section>

      {/* MISSION SECTION */}
      <section className="py-24 bg-white relative overflow-hidden">
        
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-30"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-30"></div>

        <div className="max-w-7xl mx-auto px-6 relative z-10">
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Our Mission
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Democratizing UPSC preparation with cutting-edge AI technology, 
              making world-class resources accessible to every aspirant across India.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-16 items-center">

            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-purple-400 to-blue-500 rounded-3xl blur-xl opacity-20"></div>
              <img
                src={learnImg}
                alt="Smart Study"
                className="relative w-full max-w-md mx-auto drop-shadow-xl"
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-6"
            >

              {[
                { icon: "🤖", title: "AI Current Affairs Summarizer", desc: "Digest daily news in minutes with AI-powered summaries" },
                { icon: "⚡", title: "Smart Mock Test Generator", desc: "Adaptive tests that learn from your performance" },
                { icon: "🎯", title: "Answer Evaluation System", desc: "Get instant feedback with detailed analysis" },
                { icon: "✨", title: "Personalized Learning", desc: "Custom study plans tailored to your strengths" }
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: 20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  whileHover={{ x: 10 }}
                  className="flex gap-4 p-4 rounded-2xl hover:bg-gradient-to-r hover:from-purple-50 hover:to-blue-50 transition-all cursor-pointer group"
                >
                  <div className="text-4xl group-hover:scale-110 transition-transform">{item.icon}</div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-1">{item.title}</h3>
                    <p className="text-gray-600">{item.desc}</p>
                  </div>
                </motion.div>
              ))}

            </motion.div>

          </div>

        </div>

      </section>

      {/* STATS SECTION */}
      <section className="relative bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 py-24 overflow-hidden">

        {/* Soft background glow */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/3 left-1/4 w-[32rem] h-[32rem] bg-indigo-500/15 rounded-full blur-[140px]"></div>
          <div className="absolute bottom-1/4 right-1/4 w-[28rem] h-[28rem] bg-purple-500/15 rounded-full blur-[140px]"></div>
        </div>

        <div className="max-w-7xl mx-auto px-6 relative z-10">

          {/* Heading */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
              Trusted by Thousands
            </h2>
            <p className="text-lg md:text-xl text-white/70 max-w-xl mx-auto">
              Real impact measured through student success, engagement and performance.
            </p>
          </motion.div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">

            {[
              { num: "1.7L+", label: "Active Students", icon: "👨‍🎓", color: "from-blue-400 to-cyan-400" },
              { num: "25M+", label: "AI Interactions", icon: "🤖", color: "from-violet-400 to-fuchsia-400" },
              { num: "30K+", label: "Questions Solved", icon: "📝", color: "from-emerald-400 to-teal-400" },
              { num: "99%", label: "Satisfaction Rate", icon: "⭐", color: "from-amber-400 to-yellow-400" }
            ].map((item, i) => (

              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.12, duration: 0.6 }}
                whileHover={{ y: -8 }}
                className="relative group"
              >

                {/* Glow halo */}
                <div className={`absolute -inset-0.5 bg-gradient-to-br ${item.color} opacity-20 blur-xl rounded-2xl group-hover:opacity-30 transition-opacity`}></div>

                {/* Card */}
                <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8 text-center shadow-xl hover:border-white/20 transition-all">

                  {/* Icon */}
                  <div className="text-4xl mb-4 opacity-90">
                    {item.icon}
                  </div>

                  {/* Number */}
                  <h3 className={`text-4xl md:text-5xl font-extrabold mb-2 bg-gradient-to-r ${item.color} bg-clip-text text-transparent`}>
                    {item.num}
                  </h3>

                  {/* Label */}
                  <p className="text-white/70 text-sm md:text-base font-medium tracking-wide">
                    {item.label}
                  </p>

                </div>

              </motion.div>

            ))}

          </div>

        </div>

      </section>


      {/* ================= WHY UPSC FLIP SECTION ================= */}
      <section className="py-28 bg-gradient-to-br from-slate-100 to-indigo-100">

        <div className="max-w-7xl mx-auto px-6">

          <div className="text-center mb-20">
            <h2 className="text-4xl font-bold text-gray-900 mb-3">
              Why Aspirants Choose UPSC Mastery
            </h2>
            <p className="text-gray-600">
              Real advantages. Real results.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-10">

            {[
              { icon: "🧠", front: "AI Study Plan", back: "Dynamic personalized preparation roadmap." },
              { icon: "⚡", front: "Save Time", back: "Focused learning saves hundreds of hours." },
              { icon: "🎯", front: "Rank Practice", back: "Real exam pattern mock tests." },
              { icon: "📚", front: "Verified Content", back: "Reviewed by toppers and mentors." },
              { icon: "💰", front: "Affordable", back: "Premium tools at student friendly pricing." },
              { icon: "🤝", front: "Community", back: "Peer learning and daily discussions." }
            ].map((item, i) => (

              <div key={i} className="group perspective relative">

                <div className="card-3d relative h-64">

                  {/* FRONT */}
                  <div className="card-front absolute inset-0 bg-white rounded-xl shadow-lg flex flex-col items-center justify-center">
                    <div className="text-5xl mb-3">{item.icon}</div>
                    <h3 className="text-lg font-bold text-indigo-600">
                      {item.front}
                    </h3>
                  </div>

                  {/* BACK */}
                  <div className="card-back absolute inset-0 bg-gradient-to-br from-indigo-600 to-purple-700 rounded-xl flex items-center justify-center">
                    <p className="text-white px-6 text-center">
                      {item.back}
                    </p>
                  </div>

                </div>

              </div>

            ))}

          </div>

        </div>

        <style>{`
          .perspective {
            perspective: 1200px;
          }

          .card-3d {
            transform-style: preserve-3d;
            transition: transform 0.8s ease;
          }

          .group:hover .card-3d {
            transform: rotateY(180deg);
          }

          .card-front,
          .card-back {
            backface-visibility: hidden;
          }

          .card-back {
            transform: rotateY(180deg);
          }
        `}</style>

      </section>

      {/* CTA + FOOTER WRAPPER */}
      <div className="relative overflow-hidden">

        {/* ================= CTA SECTION ================= */}
        <section className="relative py-28 bg-gradient-to-br from-indigo-700 via-purple-700 to-indigo-800">

          {/* Soft Animated Glow */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-20 left-32 w-72 h-72 bg-white/20 rounded-full blur-[120px] animate-pulse"></div>
            <div className="absolute bottom-20 right-32 w-96 h-96 bg-pink-300/20 rounded-full blur-[140px] animate-pulse delay-700"></div>
          </div>

          <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7 }}
            >
              <div className="inline-block mb-6 px-5 py-2 bg-white/15 backdrop-blur-md rounded-full text-white text-sm font-medium border border-white/20">
                🚀 AI Powered UPSC Preparation Platform
              </div>

              {/* Heading */}
              <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-6 leading-tight">
                Ready To Transform Your UPSC Preparation?
              </h2>

              {/* Subtitle */}
              <p className="text-lg md:text-xl text-white/85 mb-10 max-w-3xl mx-auto leading-relaxed">
                Join <span className="font-semibold text-white">170,000+</span> serious aspirants using AI-driven learning,
                smart mock tests and personalized study plans to crack UPSC faster and smarter.
              </p>

              {/* Buttons */}
              <div className="flex flex-wrap justify-center gap-5">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-4 bg-white text-indigo-700 rounded-full font-bold text-lg shadow-xl hover:shadow-2xl transition-all"
                >
                  Get Started Free
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-4 bg-transparent text-white rounded-full font-bold text-lg border border-white/40 hover:bg-white/10 backdrop-blur-sm transition-all"
                >
                  Schedule Live Demo
                </motion.button>
              </div>

              {/* Trust Line */}
              <p className="mt-8 text-sm text-white/70">
                ✨ No Credit Card Required • 7-Day Free Trial • Cancel Anytime
              </p>

            </motion.div>
          </div>

        </section>

        {/* ================= FOOTER SECTION ================= */}
        <footer className="bg-slate-950 text-gray-300 pt-20 pb-10">

          <div className="max-w-7xl mx-auto px-6">

            {/* TOP INFO */}
            <div className="grid md:grid-cols-3 gap-12 mb-14">
              {/* BRAND */}
              <div>
                <h3 className="text-2xl font-bold text-white mb-4">
                  UPSC Mastery
                </h3>

                <p className="text-gray-400 leading-relaxed max-w-sm">
                  AI powered IAS preparation platform helping aspirants achieve success
                  through smart learning, adaptive practice and real exam insights.
                </p>
              </div>

              {/* CONTACT */}
              <div>
                <h4 className="text-lg font-semibold text-white mb-4">
                  Contact
                </h4>

                <ul className="space-y-3 text-gray-400">
                  <li>📞 +91 6300708369</li>
                  <li>✉️ swapnakondapuram05@gmail.com</li>
                  <li>📍 India</li>
                </ul>
              </div>

              {/* SOCIAL */}
              <div>
                <h4 className="text-lg font-semibold text-white mb-4">
                  Connect With Us
                </h4>

                <div className="flex gap-4">

                  <div className="w-10 h-10 flex items-center justify-center rounded-full bg-white/10 hover:bg-indigo-600 transition cursor-pointer">
                    🌐
                  </div>

                  <div className="w-10 h-10 flex items-center justify-center rounded-full bg-white/10 hover:bg-blue-600 transition cursor-pointer">
                    💼
                  </div>

                  <div className="w-10 h-10 flex items-center justify-center rounded-full bg-white/10 hover:bg-pink-600 transition cursor-pointer">
                    📸
                  </div>

                  <div className="w-10 h-10 flex items-center justify-center rounded-full bg-white/10 hover:bg-sky-600 transition cursor-pointer">
                    🐦
                  </div>

                </div>
              </div>

            </div>

            {/* LINKS GRID */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-8 border-t border-white/10 pt-12">
              <div>
                <h5 className="font-semibold text-white mb-3">Current Affairs</h5>
                <ul className="space-y-2 text-gray-400">
                  <li>Daily News</li>
                  <li>Monthly Magazine</li>
                  <li>PIB Summary</li>
                </ul>
              </div>

              <div>
                <h5 className="font-semibold text-white mb-3">UPSC Resources</h5>
                <ul className="space-y-2 text-gray-400">
                  <li>Syllabus</li>
                  <li>PYQs</li>
                  <li>Books</li>
                  <li>Marks Calculator</li>
                </ul>
              </div>

              <div>
                <h5 className="font-semibold text-white mb-3">General Studies</h5>
                <ul className="space-y-2 text-gray-400">
                  <li>History</li>
                  <li>Polity</li>
                  <li>Economy</li>
                  <li>Geography</li>
                </ul>
              </div>

              <div>
                <h5 className="font-semibold text-white mb-3">Preparation</h5>
                <ul className="space-y-2 text-gray-400">
                  <li>Strategy</li>
                  <li>Mock Tests</li>
                  <li>Answer Writing</li>
                  <li>Interview Prep</li>
                </ul>
              </div>

              <div>
                <h5 className="font-semibold text-white mb-3">Company</h5>
                <ul className="space-y-2 text-gray-400">
                  <li>About Us</li>
                  <li>Pricing</li>
                  <li>Blogs</li>
                  <li>Privacy Policy</li>
                </ul>
              </div>

            </div>

            {/* BOTTOM BAR */}
            <div className="border-t border-white/10 mt-12 pt-6 text-center text-gray-500 text-sm">
              © 2026 UPSC Mastery • All Rights Reserved
            </div>

          </div>

        </footer>

      </div>

    </div>
  );
}