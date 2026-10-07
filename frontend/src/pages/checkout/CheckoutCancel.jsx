function CheckoutCancel() {
  return (
    <div className="min-h-screen bg-orange-50 flex items-center justify-center">
      <div className="bg-white border border-orange-200 rounded-lg p-8 text-center">
        <h1 className="text-3xl font-bold text-orange-600">
          Payment Cancelled
        </h1>

        <p className="text-gray-600 mt-3">
          Your payment was cancelled.
        </p>
      </div>
    </div>
  );
}

export default CheckoutCancel;