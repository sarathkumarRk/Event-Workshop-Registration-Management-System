import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import API from "../../api/axios";

function AdminPayments() {
  const [payments, setPayments] = useState([]);

  useEffect(() => {
    getPayments();
  }, []);

  const getPayments = async () => {
    try {
      const response = await API.get("/admin/payments");

      setPayments(response.data);
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Failed to load payments"
      );
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-7xl mx-auto">

        <h1 className="text-3xl font-bold text-orange-600 mb-6">
          Payments
        </h1>

        {payments.length === 0 ? (
          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              No payments found.
            </p>
          </div>
        ) : (
          <div className="space-y-4">

            {payments.map((payment) => (
              <div
                key={payment.id}
                className="bg-white border border-orange-200 rounded-lg p-6"
              >
                <p className="text-gray-700">
                  <span className="font-semibold">
                    Payment ID:
                  </span>{" "}
                  {payment.id}
                </p>

                <p className="text-gray-700 mt-2">
                  <span className="font-semibold">
                    Registration ID:
                  </span>{" "}
                  {payment.registration_id}
                </p>

                <p className="text-gray-700 mt-2">
                  <span className="font-semibold">
                    Amount:
                  </span>{" "}
                  ₹{payment.amount}
                </p>

                <p className="text-gray-700 mt-2">
                  <span className="font-semibold">
                    Status:
                  </span>{" "}
                  <span className="text-orange-600 font-semibold">
                    {payment.status}
                  </span>
                </p>

                <p className="text-gray-700 mt-2">
                  <span className="font-semibold">
                    Created At:
                  </span>{" "}
                  {payment.created_at}
                </p>
              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default AdminPayments;