import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import API from "../../api/axios";

function AdminDashboard() {
  const [dashboard, setDashboard] = useState({
    total_workshops: 0,
    total_registrations: 0,
    confirmed_registrations: 0,
    cancelled_registrations: 0,
    total_revenue: 0,
  });

  useEffect(() => {
    getDashboard();
  }, []);

  const getDashboard = async () => {
    try {
      const response = await API.get("/admin/dashboard");

      setDashboard(response.data);
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Failed to load dashboard"
      );
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-7xl mx-auto">

        <h1 className="text-3xl font-bold text-orange-600 mb-6">
          Admin Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              Total Workshops
            </p>

            <h2 className="text-3xl font-bold text-orange-600 mt-2">
              {dashboard.total_workshops}
            </h2>
          </div>

          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              Total Registrations
            </p>

            <h2 className="text-3xl font-bold text-orange-600 mt-2">
              {dashboard.total_registrations}
            </h2>
          </div>

          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              Confirmed Registrations
            </p>

            <h2 className="text-3xl font-bold text-orange-600 mt-2">
              {dashboard.confirmed_registrations}
            </h2>
          </div>

          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              Cancelled Registrations
            </p>

            <h2 className="text-3xl font-bold text-orange-600 mt-2">
              {dashboard.cancelled_registrations}
            </h2>
          </div>

          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              Total Revenue
            </p>

            <h2 className="text-3xl font-bold text-orange-600 mt-2">
              ₹{dashboard.total_revenue}
            </h2>
          </div>

        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;