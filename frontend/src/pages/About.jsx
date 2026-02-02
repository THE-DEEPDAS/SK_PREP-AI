import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="fixed top-0 w-full z-50 bg-white shadow-sm p-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">

        <Link to="/" className="text-2xl font-bold text-blue-600">
          UPSC Mastery
        </Link>

        <div className="flex gap-6 items-center">

          <Link to="/">Home</Link>

          <Link to="/about">About</Link>

          <Link to="/login">
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg">
              Login
            </button>
          </Link>

        </div>

      </div>
    </nav>
  );
};



const Footer = () => <footer className="bg-gray-900 text-white py-12">
  <div className="max-w-7xl mx-auto px-6 text-center">
    <p className="text-gray-400">© 2026 UPSC Mastery. All rights reserved.</p>
  </div>
</footer>;

const Testimonials = () => <div className="py-20 bg-white">
  <h2 className="text-4xl font-bold text-center mb-12">What Students Say</h2>
</div>;

const Playstore = () => <div className="py-12 bg-gray-100">
  <div className="text-center">
    <button className="px-8 py-4 bg-black text-white rounded-xl font-bold">
      Download on Play Store
    </button>
  </div>
</div>;

const SEO = ({ title, description }) => null;

const Landing = () => {
  const [activeFeature, setActiveFeature] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % 3);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="overflow-x-hidden">

      <SEO
        title="UPSC Mastery – AI Powered UPSC Preparation Platform"
        description="Prepare UPSC smarter using AI, mock tests, current affairs summarizer and intelligent tutor."
      />

      <Navbar />

      {/* HERO SECTION - Problem & Solution Focused */}
      <section className="relative min-h-screen flex items-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 pt-20">
        
        <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">
          
          {/* Left: Value Proposition */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-block mb-4 px-4 py-2 bg-blue-100 rounded-full text-blue-700 text-sm font-semibold"
            >
              Trusted by 1,70,000+ UPSC Aspirants
            </motion.div>

            <h1 className="text-5xl md:text-6xl font-bold mb-6 text-gray-900 leading-tight">
              Your AI Partner for
              <span className="block text-blue-600">UPSC Success</span>
            </h1>

            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Stop struggling with overwhelming syllabus and scattered resources. 
              Get personalized AI guidance that understands YOUR preparation needs.
            </p>

            <div className="flex flex-wrap gap-4 mb-8">
              <Link to="/login">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold text-lg shadow-lg hover:bg-blue-700 transition-colors"
                >
                  Start Free Trial
                </motion.button>
              </Link>

              
              



              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg border-2 border-blue-600 hover:bg-blue-50 transition-colors"
              >
                See How It Works
              </motion.button>
            </div>

            <div className="flex items-center gap-6 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                </svg>
                <span>7-day free trial</span>
              </div>
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                </svg>
                <span>No credit card required</span>
              </div>
            </div>

          </motion.div>

          {/* Right: Visual Showcase */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            
            {/* Main Card */}
            <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
              
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white text-xl">
                  🤖
                </div>
                <div>
                  <div className="font-bold text-gray-900">AI Study Assistant</div>
                  <div className="text-sm text-gray-500">Always ready to help</div>
                </div>
              </div>

              <div className="space-y-4">
                
                {/* User Question */}
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="text-sm text-gray-500 mb-1">You asked:</div>
                  <div className="text-gray-700">"Explain Article 370 and its implications"</div>
                </div>

                {/* AI Response Preview */}
                <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-600">
                  <div className="text-sm text-blue-700 font-semibold mb-2">AI Explanation</div>
                  <div className="text-gray-700 text-sm">Article 370 granted special autonomous status to Jammu and Kashmir...</div>
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 1.5, delay: 0.5 }}
                    className="h-1 bg-blue-600 rounded-full mt-3"
                  />
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-3 gap-3 pt-2">
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="font-bold text-blue-600">24/7</div>
                    <div className="text-xs text-gray-600">Available</div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="font-bold text-blue-600">Instant</div>
                    <div className="text-xs text-gray-600">Answers</div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="font-bold text-blue-600">Free</div>
                    <div className="text-xs text-gray-600">Trial</div>
                  </div>
                </div>

              </div>

            </div>

            {/* Floating Elements */}
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
              className="absolute -top-4 -right-4 bg-green-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg"
            >
              ✓ Live Now
            </motion.div>

          </motion.div>

        </div>

      </section>

      {/* PROBLEM SECTION */}
      <section className="py-20 bg-white">
        
        <div className="max-w-7xl mx-auto px-6">
          
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              We Understand Your Struggles
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              UPSC preparation shouldn't feel like climbing a mountain alone
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            
            {[
              {
                problem: "Information Overload",
                solution: "AI-curated daily news summaries",
                icon: "📚",
                color: "blue"
              },
              {
                problem: "No Personal Guidance",
                solution: "24/7 AI mentor tailored to you",
                icon: "🎯",
                color: "purple"
              },
              {
                problem: "Expensive Coaching",
                solution: "Premium features at 1/10th cost",
                icon: "💰",
                color: "green"
              }
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-gray-50 p-8 rounded-xl hover:shadow-lg transition-shadow"
              >
                
                <div className="text-5xl mb-4">{item.icon}</div>
                
                <div className="mb-4">
                  <div className="text-red-600 font-semibold mb-2">❌ {item.problem}</div>
                  <div className="text-green-600 font-semibold">✓ {item.solution}</div>
                </div>

                <div className={`h-1 bg-${item.color}-600 rounded-full w-12`}></div>

              </motion.div>
            ))}

          </div>

        </div>

      </section>

      {/* HOW IT HELPS - Feature Tabs */}
      <section className="py-20 bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
        
        <div className="max-w-7xl mx-auto px-6">
          
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              How We Help You Succeed
            </h2>
            <p className="text-xl text-blue-100">
              Simple, smart tools that actually work
            </p>
          </div>

          {/* Feature Tabs */}
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            {["Daily News", "Mock Tests", "Answer Writing"].map((tab, i) => (
              <button
                key={i}
                onClick={() => setActiveFeature(i)}
                className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                  activeFeature === i
                    ? "bg-white text-blue-600 shadow-lg"
                    : "bg-white/20 text-white hover:bg-white/30"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Feature Content */}
          <motion.div
            key={activeFeature}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid md:grid-cols-2 gap-12 items-center"
          >
            
            {activeFeature === 0 && (
              <>
                <div>
                  <h3 className="text-3xl font-bold mb-4">AI-Powered News Digest</h3>
                  <p className="text-blue-100 text-lg mb-6">
                    Stop wasting hours reading newspapers. Our AI reads, summarizes, and links 
                    current affairs directly to UPSC syllabus topics every single day.
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Covers all major newspapers</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Syllabus-linked summaries</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Save 2-3 hours daily</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-white/10 backdrop-blur-lg p-6 rounded-xl">
                  <div className="bg-white p-6 rounded-lg text-gray-900">
                    <div className="font-bold mb-2">Today's Top Story</div>
                    <div className="text-sm text-gray-600 mb-3">Climate Summit 2024</div>
                    <div className="bg-blue-50 p-3 rounded text-sm">
                      <div className="font-semibold text-blue-700 mb-1">Linked Topics:</div>
                      <div className="text-blue-600">GS3: Environment, International Relations</div>
                    </div>
                  </div>
                </div>
              </>
            )}

            {activeFeature === 1 && (
              <>
                <div>
                  <h3 className="text-3xl font-bold mb-4">Smart Mock Tests</h3>
                  <p className="text-blue-100 text-lg mb-6">
                    Get AI-generated tests that adapt to your performance. Focus more on 
                    weak areas and less on topics you've mastered.
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Adaptive difficulty level</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Detailed performance analytics</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Topic-wise practice</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-white/10 backdrop-blur-lg p-6 rounded-xl">
                  <div className="bg-white p-6 rounded-lg text-gray-900">
                    <div className="font-bold mb-4">Your Progress</div>
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span>Polity</span>
                          <span className="font-bold text-green-600">85%</span>
                        </div>
                        <div className="h-2 bg-gray-200 rounded-full">
                          <div className="h-full w-[85%] bg-green-500 rounded-full"></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span>Geography</span>
                          <span className="font-bold text-yellow-600">62%</span>
                        </div>
                        <div className="h-2 bg-gray-200 rounded-full">
                          <div className="h-full w-[62%] bg-yellow-500 rounded-full"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}

            {activeFeature === 2 && (
              <>
                <div>
                  <h3 className="text-3xl font-bold mb-4">AI Answer Evaluation</h3>
                  <p className="text-blue-100 text-lg mb-6">
                    Write answers and get instant, detailed feedback. Know exactly what you're 
                    doing right and where to improve before the actual exam.
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Instant scoring & feedback</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Model answers provided</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm">✓</div>
                      <span>Track writing improvement</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-white/10 backdrop-blur-lg p-6 rounded-xl">
                  <div className="bg-white p-6 rounded-lg text-gray-900">
                    <div className="font-bold mb-3">Evaluation Report</div>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm">Your Score</span>
                      <span className="text-2xl font-bold text-blue-600">7.5/10</span>
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="bg-green-50 p-2 rounded">
                        <span className="text-green-700">✓ Good introduction</span>
                      </div>
                      <div className="bg-yellow-50 p-2 rounded">
                        <span className="text-yellow-700">⚠ Add more examples</span>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}

          </motion.div>

        </div>

      </section>

      {/* PROOF SECTION */}
      <section className="py-20 bg-gray-50">
        
        <div className="max-w-6xl mx-auto px-6">
          
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Real Results from Real Aspirants
            </h2>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { num: "1,70,000+", label: "Students Trust Us" },
              { num: "25M+", label: "Doubts Resolved" },
              { num: "30,000+", label: "Daily Active Users" },
              { num: "4.8/5", label: "Average Rating" }
            ].map((stat, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-white p-6 rounded-xl shadow-md text-center"
              >
                <div className="text-3xl font-bold text-blue-600 mb-2">{stat.num}</div>
                <div className="text-gray-600 text-sm">{stat.label}</div>
              </motion.div>
            ))}
          </div>

        </div>

      </section>

      {/* CTA SECTION */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600">
        
        <div className="max-w-4xl mx-auto text-center px-6">
          
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Start Your Journey Today
          </h2>

          <p className="text-xl text-blue-100 mb-10">
            Join thousands of aspirants who are preparing smarter with AI. 
            Try it free for 7 days.
          </p>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-12 py-5 bg-white text-blue-600 rounded-lg font-bold text-lg shadow-2xl hover:shadow-3xl transition-all"
          >
            Get Started - It's Free
          </motion.button>

          <p className="text-blue-100 mt-6 text-sm">
            No credit card required • Cancel anytime • Full access during trial
          </p>

        </div>

      </section>

      <Testimonials />
      <Playstore />
      <Footer />

    </div>
  );
};

export default Landing;