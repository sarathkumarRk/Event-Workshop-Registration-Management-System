import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import API from "../../api/axios";

function WorkshopList() {
  const [workshops, setWorkshops] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);

  const limit = 6;

  const getWorkshops = async () => {
    try {
      setLoading(true);

      const response = await API.get("/workshops", {
        params: {
          page,
          limit,
          search: search || undefined,
        },
      });

      setWorkshops(response.data.items);
      setTotalPages(response.data.total_pages);
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
  }, [page, search]);

  const handleSearch = (e) => {
    setSearch(e.target.value);
    setPage(1);
  };

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-orange-600">
            Workshops
          </h1>

          <p className="text-gray-600 mt-1">
            Find and register for available workshops
          </p>
        </div>

        <div className="mb-6">
          <input
            type="text"
            value={search}
            onChange={handleSearch}
            placeholder="Search workshop by title..."
            className="w-full md:w-96 border border-gray-300 rounded-md px-4 py-3 focus:outline-none focus:border-orange-500"
          />
        </div>

        {loading ? (
          <div className="text-center py-10">
            <p className="text-orange-600 font-semibold">
              Loading workshops...
            </p>
          </div>
        ) : workshops.length === 0 ? (
          <div className="bg-white border border-orange-200 rounded-lg p-8 text-center">
            <p className="text-gray-500">
              No workshops found.
            </p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {workshops.map((workshop) => (
                <div
                  key={workshop.id}
                  className="bg-white border border-orange-200 rounded-lg p-6"
                >
                  <div className="flex justify-between items-start gap-3">
                    <h2 className="text-xl font-semibold text-gray-800">
                      {workshop.title}
                    </h2>

                    <span className="text-sm bg-orange-100 text-orange-600 px-3 py-1 rounded-full">
                      {workshop.status}
                    </span>
                  </div>

                  <p className="text-gray-600 mt-3">
                    {workshop.description}
                  </p>

                  <div className="mt-4 space-y-2 text-sm text-gray-600">
                    <p>
                      <span className="font-semibold">
                        Speaker:
                      </span>{" "}
                      {workshop.speaker}
                    </p>

                    <p>
                      <span className="font-semibold">
                        Date:
                      </span>{" "}
                      {workshop.date}
                    </p>

                    <p>
                      <span className="font-semibold">
                        Time:
                      </span>{" "}
                      {workshop.start_time} - {workshop.end_time}
                    </p>

                    <p>
                      <span className="font-semibold">
                        Price:
                      </span>{" "}
                      ₹{workshop.price}
                    </p>

                    <p>
                      <span className="font-semibold">
                        Available Seats:
                      </span>{" "}
                      {workshop.available_seats}
                    </p>
                  </div>

                  <Link
                    to={`/workshops/${workshop.id}`}
                    className="block text-center bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-md mt-5 font-semibold"
                  >
                    View Workshop
                  </Link>
                </div>
              ))}
            </div>

            {totalPages > 0 && (
              <div className="flex justify-center items-center gap-2 mt-8">
                <button
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                  className="px-4 py-2 border border-orange-500 text-orange-600 rounded-md disabled:opacity-40"
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
                  className="px-4 py-2 border border-orange-500 text-orange-600 rounded-md disabled:opacity-40"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default WorkshopList;