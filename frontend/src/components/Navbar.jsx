import { useState } from "react";
import { Link } from "react-router-dom";
import MobileNav from "./MobileNav";

export default function Navbar() {

  const [open, setOpen] = useState(false);

  return (
    <nav className="bg-white shadow sticky top-0 z-50">

      <div className="max-w-7xl mx-auto flex justify-between items-center p-4">

        <h1 className="font-bold text-blue-600 text-xl">
          UPSC Mastery
        </h1>

        {/* Desktop */}
        <div className="hidden md:flex gap-6 items-center">

          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/download">Download</Link>

          <Link to="/login">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg">
              Login
            </button>
          </Link>

        </div>

        {/* Mobile */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden text-2xl"
        >
          ☰
        </button>

      </div>

      {open && <MobileNav close={() => setOpen(false)} />}

    </nav>
  );
}