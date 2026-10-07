import stripe

from app.config import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(
    registration_id: int,
    workshop_title: str,
    amount: float,
    participant_email: str
):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",

        customer_email=participant_email,

        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": workshop_title,
                    },
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }
        ],

        metadata={
            "registration_id": str(registration_id),
        },

        success_url=(
            "http://localhost:5173/checkout/success"
            "?session_id={CHECKOUT_SESSION_ID}"
        ),

        cancel_url=(
            "http://localhost:5173/checkout/cancel"
        ),
    )

    return session