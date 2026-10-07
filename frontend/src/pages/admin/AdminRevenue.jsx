import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import API from "../../api/axios";

function AdminRevenue() {
  const [revenue, setRevenue] = useState(0);

  useEffect(() => {
    getRevenue();
  }, []);

  const getRevenue = async () => {
    try {
      const response = await API.get("/admin/revenue");

      setRevenue(response.data.total_revenue);
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Failed to load revenue"
      );
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-2xl mx-auto">

        <h1 className="text-3xl font-bold text-orange-600 mb-6">
          Revenue
        </h1>

        <div className="bg-white border border-orange-200 rounded-lg p-8">
          <p className="text-gray-500">
            Total Revenue
          </p>

          <h2 className="text-4xl font-bold text-orange-600 mt-2">
            ₹{revenue}
          </h2>
        </div>

      </div>
    </div>
  );
}

export default AdminRevenue;