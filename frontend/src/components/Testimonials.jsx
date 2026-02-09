import { motion } from "framer-motion";

export default function Testimonials() {

  const reviews = [
    "Best AI app for UPSC preparation!",
    "Saved my revision time drastically",
    "Mock tests are very realistic",
    "Current affairs summaries are gold"
  ];

  return (
    <section className="py-20 bg-white">

      <h2 className="text-3xl font-bold text-center mb-10">
        What Aspirants Say ❤️
      </h2>

      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-6 px-6">

        {reviews.map((r, i) => (

          <motion.div
            key={i}
            whileHover={{ scale: 1.03 }}
            className="p-6 bg-gray-100 rounded-xl shadow"
          >
            “{r}”
          </motion.div>

        ))}

      </div>

    </section>
  );
}