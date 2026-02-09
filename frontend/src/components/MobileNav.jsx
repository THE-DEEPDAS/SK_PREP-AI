import { Link } from "react-router-dom";

export default function MobileNav({ open, setOpen }) {
  return (
    <div className="md:hidden bg-white shadow-lg absolute top-16 left-0 w-full z-50">

      <a href="/" className="block px-6 py-4 border-b">Home</a>
      <a href="/about" className="block px-6 py-4 border-b">About</a>
      <a href="/download" className="block px-6 py-4 border-b">Download</a>
      <a href="/login" className="block px-6 py-4">Login</a>

    </div>
  );
}