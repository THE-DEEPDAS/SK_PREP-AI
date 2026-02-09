import { Outlet, Link } from "react-router-dom";

const DashboardLayout = () => {

  const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className="flex h-screen bg-gray-100">

      {/* Sidebar */}
      <div className="w-64 bg-blue-700 text-white p-6">

        <h2 className="text-xl font-bold mb-8">
          UPSC Mastery
        </h2>

        <ul className="space-y-4">

          <Link to="/dashboard/current">
            <li className="hover:bg-blue-600 p-2 rounded cursor-pointer">
              📢 Current Affairs
            </li>
          </Link>

          <Link to="/dashboard/mocks">
            <li className="hover:bg-blue-600 p-2 rounded cursor-pointer">
              📝 Mock Tests
            </li>
          </Link>

          <Link to="/dashboard/ai">
            <li className="hover:bg-blue-600 p-2 rounded cursor-pointer">
              🤖 AI Assistant
            </li>
          </Link>

          <Link to="/dashboard/performance">
            <li className="hover:bg-blue-600 p-2 rounded cursor-pointer">
              📊 Performance
            </li>
          </Link>

        </ul>

        <button
          onClick={logout}
          className="mt-10 bg-red-500 w-full py-2 rounded"
        >
          Logout
        </button>

      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 p-6 overflow-y-auto">

        {/* This renders your module pages */}
        <Outlet />

      </div>

    </div>
  );
};

export default DashboardLayout;