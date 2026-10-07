import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import API from "../../api/axios";

function AdminParticipants() {
  const [participants, setParticipants] = useState([]);

  useEffect(() => {
    getParticipants();
  }, []);

  const getParticipants = async () => {
    try {
      const response = await API.get("/admin/participants");

      setParticipants(response.data);
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Failed to load participants"
      );
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-7xl mx-auto">

        <h1 className="text-3xl font-bold text-orange-600 mb-6">
          Participants
        </h1>

        {participants.length === 0 ? (
          <div className="bg-white border border-orange-200 rounded-lg p-6">
            <p className="text-gray-500">
              No participants found.
            </p>
          </div>
        ) : (
          <div className="space-y-4">

            {participants.map((participant) => (
              <div
                key={participant.id}
                className="bg-white border border-orange-200 rounded-lg p-6"
              >
                <p className="text-gray-700">
                  <span className="font-semibold">
                    Name:
                  </span>{" "}
                  {participant.full_name}
                </p>

                <p className="text-gray-700 mt-2">
                  <span className="font-semibold">
                    Email:
                  </span>{" "}
                  {participant.email}
                </p>

                <p className="text-gray-700 mt-2">
                  <span className="font-semibold">
                    Role:
                  </span>{" "}
                  {participant.role}
                </p>

                <p className="text-gray-700 mt-2">
                  <span className="font-semibold">
                    Created At:
                  </span>{" "}
                  {participant.created_at}
                </p>
              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default AdminParticipants;