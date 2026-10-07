import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import API from "../../api/axios";

function AdminWorkshops() {
  const [workshops, setWorkshops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    title: "",
    description: "",
    speaker: "",
    date: "",
    start_time: "",
    end_time: "",
    price: "",
    capacity: "",
  });

  const getWorkshops = async () => {
    try {
      const response = await API.get("/workshops");
      setWorkshops(response.data.items);
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Failed to load workshops"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getWorkshops();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const resetForm = () => {
    setForm({
      title: "",
      description: "",
      speaker: "",
      date: "",
      start_time: "",
      end_time: "",
      price: "",
      capacity: "",
    });

    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      title: form.title,
      description: form.description,
      speaker: form.speaker,
      date: form.date,
      start_time: form.start_time,
      end_time: form.end_time,
      price: Number(form.price),
      capacity: Number(form.capacity),
    };

    try {
      if (editingId) {
        await API.put(`/workshops/${editingId}`, data);
        toast.success("Workshop updated");
      } else {
        await API.post("/workshops", data);
        toast.success("Workshop created");
      }

      resetForm();
      getWorkshops();
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Workshop operation failed"
      );
    }
  };

  const editWorkshop = (workshop) => {
    setEditingId(workshop.id);

    setForm({
      title: workshop.title,
      description: workshop.description,
      speaker: workshop.speaker,
      date: workshop.date,
      start_time: workshop.start_time,
      end_time: workshop.end_time,
      price: workshop.price,
      capacity: workshop.capacity,
    });
  };

  const deleteWorkshop = async (id) => {
    try {
      await API.delete(`/workshops/${id}`);

      toast.success("Workshop deleted");

      getWorkshops();
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Failed to delete workshop"
      );
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-orange-600 font-semibold">
          Loading workshops...
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-orange-600 mb-6">
          Manage Workshops
        </h1>

        <div className="bg-white border border-orange-200 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-5">
            {editingId ? "Update Workshop" : "Create Workshop"}
          </h2>

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 md:grid-cols-2 gap-4"
          >
            <input
              type="text"
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="Workshop Title"
              required
              className="border border-gray-300 rounded-md px-4 py-3"
            />

            <input
              type="text"
              name="speaker"
              value={form.speaker}
              onChange={handleChange}
              placeholder="Speaker"
              required
              className="border border-gray-300 rounded-md px-4 py-3"
            />

            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Description"
              required
              className="border border-gray-300 rounded-md px-4 py-3 md:col-span-2"
            />

            <input
              type="date"
              name="date"
              value={form.date}
              onChange={handleChange}
              required
              className="border border-gray-300 rounded-md px-4 py-3"
            />

            <input
              type="time"
              name="start_time"
              value={form.start_time}
              onChange={handleChange}
              required
              className="border border-gray-300 rounded-md px-4 py-3"
            />

            <input
              type="time"
              name="end_time"
              value={form.end_time}
              onChange={handleChange}
              required
              className="border border-gray-300 rounded-md px-4 py-3"
            />

            <input
              type="number"
              name="price"
              value={form.price}
              onChange={handleChange}
              placeholder="Price"
              min="0"
              required
              className="border border-gray-300 rounded-md px-4 py-3"
            />

            <input
              type="number"
              name="capacity"
              value={form.capacity}
              onChange={handleChange}
              placeholder="Capacity"
              min="1"
              required
              className="border border-gray-300 rounded-md px-4 py-3"
            />

            <button
              type="submit"
              className="bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-md font-semibold"
            >
              {editingId ? "Update Workshop" : "Create Workshop"}
            </button>

            {editingId && (
              <button
                type="button"
                onClick={resetForm}
                className="border border-orange-500 text-orange-600 py-3 rounded-md font-semibold"
              >
                Cancel
              </button>
            )}
          </form>
        </div>

        <div className="bg-white border border-orange-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-5">
            Workshops
          </h2>

          {workshops.length === 0 ? (
            <p className="text-gray-500">
              No workshops found.
            </p>
          ) : (
            <div className="space-y-4">
              {workshops.map((workshop) => (
                <div
                  key={workshop.id}
                  className="border border-gray-200 rounded-lg p-5"
                >
                  <div className="flex flex-col md:flex-row md:justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-800">
                        {workshop.title}
                      </h3>

                      <p className="text-gray-600 mt-1">
                        {workshop.description}
                      </p>

                      <p className="text-gray-600 mt-2">
                        Speaker: {workshop.speaker}
                      </p>

                      <p className="text-gray-600">
                        Date: {workshop.date}
                      </p>

                      <p className="text-gray-600">
                        Time: {workshop.start_time} - {workshop.end_time}
                      </p>

                      <p className="text-gray-600">
                        Price: ₹{workshop.price}
                      </p>

                      <p className="text-gray-600">
                        Capacity: {workshop.capacity}
                      </p>

                      <p className="text-gray-600">
                        Available Seats: {workshop.available_seats}
                      </p>

                      <p className="text-orange-600 font-semibold mt-1">
                        Status: {workshop.status}
                      </p>
                    </div>

                    <div className="flex gap-3 items-start">
                      <button
                        onClick={() => editWorkshop(workshop)}
                        className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md"
                      >
                        Edit
                      </button>

                      <button
                        onClick={() => deleteWorkshop(workshop.id)}
                        className="border border-orange-500 text-orange-600 px-4 py-2 rounded-md"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminWorkshops;