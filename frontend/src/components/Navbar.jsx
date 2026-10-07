import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const token = localStorage.getItem("access_token");
  const role = localStorage.getItem("user_role");

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");

    navigate("/login");
  };

  if (!token) {
    return null;
  }

  return (
    <nav className="bg-white border-b border-orange-200">
      <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">

        <Link
          to={
            role === "admin"
              ? "/admin/dashboard"
              : "/workshops"
          }
          className="text-2xl font-bold text-orange-600"
        >
          Event Workshop
        </Link>

        <div className="flex flex-wrap items-center gap-4">

          {role === "participant" && (
            <>
              <Link
                to="/workshops"
                className="text-gray-700 hover:text-orange-600"
              >
                Workshops
              </Link>

              <Link
                to="/registrations"
                className="text-gray-700 hover:text-orange-600"
              >
                My Registrations
              </Link>
            </>
          )}

          {role === "admin" && (
            <>
              <Link
                to="/admin/dashboard"
                className="text-gray-700 hover:text-orange-600"
              >
                Dashboard
              </Link>

              <Link
                to="/admin/workshops"
                className="text-gray-700 hover:text-orange-600"
              >
                Workshops
              </Link>

              <Link
                to="/admin/participants"
                className="text-gray-700 hover:text-orange-600"
              >
                Participants
              </Link>

              <Link
                to="/admin/payments"
                className="text-gray-700 hover:text-orange-600"
              >
                Payments
              </Link>

              <Link
                to="/admin/revenue"
                className="text-gray-700 hover:text-orange-600"
              >
                Revenue
              </Link>
            </>
          )}

          <button
            onClick={logout}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md"
          >
            Logout
          </button>

        </div>
      </div>
    </nav>
  );
}

export default Navbar;