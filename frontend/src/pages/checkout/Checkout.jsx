import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "react-toastify";
import API from "../../api/axios";

function Checkout() {
  const [searchParams] = useSearchParams();

  useEffect(() => {
    createCheckoutSession();
  }, []);

  const createCheckoutSession = async () => {
    const registrationId = searchParams.get("registration_id");

    try {
      const response = await API.post(
        `/payments/create-checkout-session?registration_id=${registrationId}`
      );

      window.location.href = response.data.checkout_url;
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Payment failed"
      );
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 flex items-center justify-center">
      <p className="text-orange-600 font-semibold">
        Redirecting to payment...
      </p>
    </div>
  );
}

export default Checkout;