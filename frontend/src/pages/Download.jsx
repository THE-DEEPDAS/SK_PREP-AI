import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import SEO from "../components/SEO";
import { motion } from "framer-motion";


export default function Download() {

  return (
    <div>

      <SEO
        title="Download UPSC Mastery App"
        description="Download UPSC Mastery AI app and start smart IAS preparation today."
      />

      <Navbar />

      {/* HERO DOWNLOAD */}
      <section className="bg-gradient-to-br from-purple-600 to-blue-600 py-20 text-white">

        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-10 items-center px-6">

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
          >

            <h1 className="text-4xl font-bold mb-4">
              Download UPSC Mastery App
            </h1>

            <p className="mb-6 text-lg">
              AI Powered Study Companion for UPSC Aspirants
            </p>

            <div className="flex gap-4">

              <button className="bg-black px-6 py-3 rounded-lg">
                Google Play
              </button>

              <button className="bg-black px-6 py-3 rounded-lg">
                App Store
              </button>

            </div>

          </motion.div>

          <motion.img
            whileHover={{ scale: 1.05 }}
            src={phoneImg}
            alt="Mobile App"
            className="w-full max-w-sm mx-auto"
          />

        </div>

      </section>

      {/* FEATURES */}
      <section className="py-20 bg-white">

        <h2 className="text-3xl font-bold text-center mb-12">
          Why Download UPSC Mastery?
        </h2>

        <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-6 px-6">

          {[
            "AI Based Current Affairs",
            "Smart Mock Tests",
            "Answer Writing Evaluator",
            "Daily News Summary",
            "NCERT AI Tutor",
            "Revision Planner"
          ].map((f, i) => (

            <motion.div
              key={i}
              whileHover={{ scale: 1.05 }}
              className="bg-gray-100 p-6 rounded-xl shadow text-center"
            >

              <h3 className="font-bold">
                {f}
              </h3>

            </motion.div>

          ))}

        </div>

      </section>

      {/* CTA */}
      <section className="bg-gray-900 text-white py-20 text-center">

        <h2 className="text-3xl font-bold mb-4">
          Start Smart Preparation Today
        </h2>

        <p className="mb-6">
          Join thousands of aspirants preparing with AI
        </p>

        <button className="bg-blue-600 px-8 py-4 rounded-xl text-lg">
          Download Now
        </button>

      </section>

      <Footer />

    </div>
  );
}