import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import SEO from "../components/SEO";

const Login = () => {

  const navigate = useNavigate();

  const [mode, setMode] = useState("signin");

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  // ✅ FIXED LOGIN HANDLER
  const handleSubmit = (e) => {
    e.preventDefault();

    if (form.email && form.password) {

      // Save login session (demo)
      localStorage.setItem("token", "loggedin");

      // Redirect to Dashboard
      navigate("/dashboard");

    } else {
      alert("Fill all required fields");
    }
  };

  return (
    <div>

      <SEO
        title="Login | UPSC Mastery"
        description="Sign in or create account on UPSC Mastery AI platform."
      />

      <Navbar />

      {/* AUTH CONTAINER */}
      <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">



{/* Animated Background */}
        <div className="absolute inset-0 animated-bg"></div>


{/* Soft Glow Layer */}
<div className="absolute inset-0 bg-black/20 backdrop-blur-sm"></div>


{/* Login Card */}
<div className="relative bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl w-full max-w-md p-8 animate-fadeIn">


{/* HEADER */}
<div className="text-center mb-6">
<h2 className="text-3xl font-bold text-gray-800">
UPSC Mastery
</h2>
<p className="text-gray-500 mt-1">
AI Powered Preparation Platform
</p>
</div>

          {/* TOGGLE */}
          <div className="flex bg-gray-100 rounded-xl p-1 mb-6">

            <button
              onClick={() => setMode("signin")}
              className={`w-1/2 py-2 rounded-xl font-semibold ${
                mode === "signin"
                  ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white"
                  : "text-gray-600"
              }`}
            >
              Sign In
            </button>

            <button
              onClick={() => setMode("signup")}
              className={`w-1/2 py-2 rounded-xl font-semibold ${
                mode === "signup"
                  ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white"
                  : "text-gray-600"
              }`}
            >
              Sign Up
            </button>

          </div>

          {/* FORM */}
          <form onSubmit={handleSubmit} className="space-y-4">

            {mode === "signup" && (
              <input
                type="text"
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="Full Name"
                className="w-full px-4 py-3 border rounded-xl"
              />
            )}

            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="Email"
              className="w-full px-4 py-3 border rounded-xl"
            />

            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Password"
              className="w-full px-4 py-3 border rounded-xl"
            />

            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold"
            >
              {mode === "signin" ? "Sign In" : "Create Account"}
            </button>

          </form>

        </div>

      </div>

      <Footer />
      {/* Component Scoped Styles */}
<style>{`
.animated-bg {
background: linear-gradient(
-45deg,
#020617,
#0f172a,
#1e3a8a,
#312e81
);
background-size: 400% 400%;
animation: gradientMove 18s ease infinite;
}


@keyframes gradientMove {
0% {
background-position: 0% 50%;
}
50% {
background-position: 100% 50%;
}
100% {
background-position: 0% 50%;
}
}


@keyframes fadeIn {
from {
opacity: 0;
transform: translateY(25px);
}
to {
opacity: 1;
transform: translateY(0);
}
}


.animate-fadeIn {
animation: fadeIn 0.6s ease-out;
}
`}</style>




    </div>
  );
};

export default Login;