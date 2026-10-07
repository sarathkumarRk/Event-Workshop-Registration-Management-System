import { Routes, Route } from "react-router-dom";

import ProtectedRoute from "../components/ProtectedRoute";

import Login from "../pages/Login";
import Register from "../pages/Register";

import WorkshopList from "../pages/workshops/WorkshopList";
import WorkshopDetails from "../pages/workshops/WorkshopDetails";

import Checkout from "../pages/checkout/Checkout";
import CheckoutSuccess from "../pages/checkout/CheckoutSuccess";
import CheckoutCancel from "../pages/checkout/CheckoutCancel";

import RegistrationList from "../pages/registrations/RegistrationList";
import RegistrationDetails from "../pages/registrations/RegistrationDetails";

import AdminDashboard from "../pages/admin/AdminDashboard";
import AdminParticipants from "../pages/admin/AdminParticipants";
import AdminPayments from "../pages/admin/AdminPayments";
import AdminRevenue from "../pages/admin/AdminRevenue";
import AdminWorkshops from "../pages/admin/AdminWorkshops";

function AppRoutes() {
  return (
    <Routes>

      {/* Home */}

      <Route
        path="/"
        element={<Login />}
      />


      {/* Public Routes */}

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />


      {/* Participant + Admin Routes */}

      <Route
        path="/workshops"
        element={
          <ProtectedRoute>
            <WorkshopList />
          </ProtectedRoute>
        }
      />

      <Route
        path="/workshops/:id"
        element={
          <ProtectedRoute>
            <WorkshopDetails />
          </ProtectedRoute>
        }
      />

      <Route
        path="/registrations"
        element={
          <ProtectedRoute>
            <RegistrationList />
          </ProtectedRoute>
        }
      />

      <Route
        path="/registrations/:id"
        element={
          <ProtectedRoute>
            <RegistrationDetails />
          </ProtectedRoute>
        }
      />


      {/* Participant Routes */}

      <Route
        path="/checkout"
        element={
          <ProtectedRoute role="participant">
            <Checkout />
          </ProtectedRoute>
        }
      />

      <Route
        path="/checkout/success"
        element={
          <ProtectedRoute role="participant">
            <CheckoutSuccess />
          </ProtectedRoute>
        }
      />

      <Route
        path="/checkout/cancel"
        element={
          <ProtectedRoute role="participant">
            <CheckoutCancel />
          </ProtectedRoute>
        }
      />


      {/* Admin Routes */}

      <Route
        path="/admin/dashboard"
        element={
          <ProtectedRoute role="admin">
            <AdminDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/workshops"
        element={
          <ProtectedRoute role="admin">
            <AdminWorkshops />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/participants"
        element={
          <ProtectedRoute role="admin">
            <AdminParticipants />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/payments"
        element={
          <ProtectedRoute role="admin">
            <AdminPayments />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/revenue"
        element={
          <ProtectedRoute role="admin">
            <AdminRevenue />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}

export default AppRoutes;