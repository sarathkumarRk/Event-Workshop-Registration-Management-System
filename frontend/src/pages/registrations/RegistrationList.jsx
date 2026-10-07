import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import API from "../../api/axios";

function RegistrationList() {
  const [registrations, setRegistrations] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  const limit = 10;

  const getRegistrations = async () => {
    try {
      const response = await API.get("/registrations", {
        params: {
          page,
          limit,
        },
      });

      setRegistrations(response.data.items);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Failed to load registrations"
      );
    }
  };

  useEffect(() => {
    getRegistrations();
  }, [page]);

  const cancelRegistration = async (id) => {
    try {
      await API.delete(`/registrations/${id}`);

      toast.success("Registration cancelled");

      getRegistrations();
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Registration cancellation failed"
      );
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-7xl mx-auto">

        <h1 className="text-3xl font-bold text-orange-600 mb-6">
          My Registrations
        </h1>

        {registrations.length === 0 ? (
          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              No registrations found.
            </p>
          </div>
        ) : (
          <div className="space-y-4">

            {registrations.map((registration) => (
              <div
                key={registration.id}
                className="bg-white border border-orange-200 rounded-lg p-6"
              >
                <p className="text-gray-700">
                  Registration ID:{" "}
                  <span className="font-semibold">
                    {registration.id}
                  </span>
                </p>

                <p className="text-gray-700 mt-2">
                  Workshop ID:{" "}
                  <span className="font-semibold">
                    {registration.workshop_id}
                  </span>
                </p>

                <p className="text-gray-700 mt-2">
                  Status:{" "}
                  <span className="text-orange-600 font-semibold">
                    {registration.status}
                  </span>
                </p>

                <p className="text-gray-700 mt-2">
                  Registered At:{" "}
                  {registration.registered_at}
                </p>

                {registration.cancelled_at && (
                  <p className="text-gray-700 mt-2">
                    Cancelled At:{" "}
                    {registration.cancelled_at}
                  </p>
                )}

                <div className="flex gap-3 mt-5">
                  <Link
                    to={`/registrations/${registration.id}`}
                    className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md"
                  >
                    View Details
                  </Link>

                  {registration.status !== "CANCELLED" && (
                    <button
                      onClick={() =>
                        cancelRegistration(registration.id)
                      }
                      className="border border-orange-500 text-orange-600 px-4 py-2 rounded-md"
                    >
                      Cancel
                    </button>
                  )}
                </div>
              </div>
            ))}

          </div>
        )}

        {totalPages > 0 && (
          <div className="flex justify-center items-center gap-2 mt-8">

            <button
              onClick={() => setPage(page - 1)}
              disabled={page === 1}
              className="px-4 py-2 border border-orange-500 text-orange-600 rounded-md disabled:opacity-50"
            >
              Previous
            </button>

            {Array.from(
              { length: totalPages },
              (_, index) => index + 1
            ).map((pageNumber) => (
              <button
                key={pageNumber}
                onClick={() => setPage(pageNumber)}
                className={`px-4 py-2 rounded-md ${
                  page === pageNumber
                    ? "bg-orange-500 text-white"
                    : "border border-orange-500 text-orange-600"
                }`}
              >
                {pageNumber}
              </button>
            ))}

            <button
              onClick={() => setPage(page + 1)}
              disabled={page === totalPages}
              className="px-4 py-2 border border-orange-500 text-orange-600 rounded-md disabled:opacity-50"
            >
              Next
            </button>

          </div>
        )}

      </div>
    </div>
  );
}

export default RegistrationList;