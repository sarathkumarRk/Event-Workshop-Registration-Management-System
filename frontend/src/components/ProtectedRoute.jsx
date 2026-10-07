import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, role }) {
  const token = localStorage.getItem("access_token");
  const userRole = localStorage.getItem("user_role");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (role && userRole !== role) {
    return <Navigate to="/workshops" replace />;
  }

  return children;
}

export default ProtectedRoute;