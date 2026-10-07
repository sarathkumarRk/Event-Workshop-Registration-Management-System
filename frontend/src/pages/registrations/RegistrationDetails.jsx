import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import API from "../../api/axios";

function RegistrationDetails() {
  const { id } = useParams();

  const [registration, setRegistration] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getRegistration();
  }, [id]);

  const getRegistration = async () => {
    try {
      const response = await API.get(
        `/registrations/${id}`
      );

      setRegistration(response.data);
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Failed to load registration"
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-orange-600 font-semibold">
          Loading registration...
        </p>
      </div>
    );
  }

  if (!registration) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-gray-600">
          Registration not found.
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-2xl mx-auto">

        <div className="bg-white border border-orange-200 rounded-lg p-8">

          <h1 className="text-3xl font-bold text-orange-600 mb-6">
            Registration Details
          </h1>

          <div className="space-y-4">

            <p className="text-gray-700">
              <span className="font-semibold">
                Registration ID:
              </span>{" "}
              {registration.id}
            </p>

            <p className="text-gray-700">
              <span className="font-semibold">
                User ID:
              </span>{" "}
              {registration.user_id}
            </p>

            <p className="text-gray-700">
              <span className="font-semibold">
                Workshop ID:
              </span>{" "}
              {registration.workshop_id}
            </p>

            <p className="text-gray-700">
              <span className="font-semibold">
                Status:
              </span>{" "}
              <span className="text-orange-600 font-semibold">
                {registration.status}
              </span>
            </p>

            <p className="text-gray-700">
              <span className="font-semibold">
                Registered At:
              </span>{" "}
              {registration.registered_at}
            </p>

            {registration.cancelled_at && (
              <p className="text-gray-700">
                <span className="font-semibold">
                  Cancelled At:
                </span>{" "}
                {registration.cancelled_at}
              </p>
            )}

          </div>

        </div>

      </div>
    </div>
  );
}

export default RegistrationDetails;