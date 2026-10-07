import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import API from "../../api/axios";

function WorkshopDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [workshop, setWorkshop] = useState(null);
  const [loading, setLoading] = useState(true);
  const [registering, setRegistering] = useState(false);

  useEffect(() => {
    getWorkshop();
  }, [id]);

  const getWorkshop = async () => {
    try {
      const response = await API.get(`/workshops/${id}`);

      setWorkshop(response.data);
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Failed to load workshop"
      );
    } finally {
      setLoading(false);
    }
  };

  const registerWorkshop = async () => {
    try {
      setRegistering(true);

      const response = await API.post("/registrations", {
        workshop_id: Number(id),
      });

      toast.success("Registration successful");

      navigate(`/checkout?registration_id=${response.data.id}`);
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Registration failed"
      );
    } finally {
      setRegistering(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-orange-600 font-semibold">
          Loading workshop...
        </p>
      </div>
    );
  }

  if (!workshop) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-gray-600">
          Workshop not found.
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white border border-orange-200 rounded-lg p-8">
          <div className="flex flex-col md:flex-row md:justify-between gap-4">
            <h1 className="text-3xl font-bold text-orange-600">
              {workshop.title}
            </h1>

            <span className="h-fit bg-orange-100 text-orange-600 px-4 py-2 rounded-full font-semibold">
              {workshop.status}
            </span>
          </div>

          <p className="text-gray-600 mt-6">
            {workshop.description}
          </p>

          <div className="mt-8 space-y-4">
            <div>
              <p className="text-sm text-gray-500">
                Speaker
              </p>
              <p className="font-semibold text-gray-800">
                {workshop.speaker}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">
                Date
              </p>
              <p className="font-semibold text-gray-800">
                {workshop.date}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">
                Time
              </p>
              <p className="font-semibold text-gray-800">
                {workshop.start_time} - {workshop.end_time}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">
                Price
              </p>
              <p className="font-semibold text-gray-800">
                ₹{workshop.price}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">
                Available Seats
              </p>
              <p className="font-semibold text-gray-800">
                {workshop.available_seats}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">
                Capacity
              </p>
              <p className="font-semibold text-gray-800">
                {workshop.capacity}
              </p>
            </div>
          </div>

          <button
            onClick={registerWorkshop}
            disabled={
              registering ||
              workshop.available_seats <= 0 ||
              workshop.status === "CANCELLED"
            }
            className="w-full mt-8 bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-md font-semibold disabled:opacity-50"
          >
            {registering
              ? "Registering..."
              : workshop.available_seats <= 0
              ? "Workshop is Full"
              : "Register Now"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default WorkshopDetails;