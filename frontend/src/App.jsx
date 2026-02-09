import { BrowserRouter, Routes, Route } from "react-router-dom";

import Landing from "./pages/Landing";
import About from "./pages/About";
import Download from "./pages/Download";
import Login from "./pages/Login";
import DashboardApp from "./pages/DashboardApp";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Landing />} />
        <Route path="/about" element={<About />} />
        <Route path="/download" element={<Download />} />
        <Route path="/login" element={<Login />} />

        {/* MAIN DASHBOARD */}
        <Route path="/dashboard" element={<DashboardApp />} />

        {/* 404 */}
        <Route path="*" element={<NotFound />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;