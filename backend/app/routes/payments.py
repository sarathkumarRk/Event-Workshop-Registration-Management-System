import stripe

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependency import participant_required
from app.models.user import User
from app.models.registration import Registration
from app.models.payment import Payment
from app.models.workshop import Workshop
from app.schemas.payment import CheckoutSessionResponse
from app.services.email_service import send_payment_confirmation_email


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


stripe.api_key = settings.STRIPE_SECRET_KEY


# Create Stripe Checkout Session

@router.post(
    "/create-checkout-session",
    response_model=CheckoutSessionResponse
)
def create_checkout_session(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(participant_required)
):
    registration = (
        db.query(Registration)
        .filter(
            Registration.id == registration_id
        )
        .first()
    )

    if registration is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )

    # Participant can pay only for own registration

    if registration.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only pay for your own registration"
        )

    # Payment is allowed only for pending registration

    if registration.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment is not available for this registration"
        )

    workshop = (
        db.query(Workshop)
        .filter(
            Workshop.id == registration.workshop_id
        )
        .first()
    )

    if workshop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found"
        )

    # Check existing payment

    existing_payment = (
        db.query(Payment)
        .filter(
            Payment.registration_id == registration.id
        )
        .first()
    )

    if existing_payment and existing_payment.status == "SUCCESS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already completed"
        )

    # Create Stripe Checkout Session

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            customer_email=current_user.email,

            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": workshop.title
                        },
                        "unit_amount": int(
                            workshop.price * 100
                        )
                    },
                    "quantity": 1
                }
            ],

            metadata={
                "registration_id": str(
                    registration.id
                )
            },

            success_url=(
                "http://localhost:5173/checkout/success"
            ),

            cancel_url=(
                "http://localhost:5173/checkout/cancel"
            )
        )

    except stripe.error.StripeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create Stripe checkout session"
        )

    # Create or update Payment record

    if existing_payment:
        payment = existing_payment

        payment.amount = workshop.price
        payment.status = "PENDING"
        payment.stripe_session_id = session.id
        payment.stripe_payment_intent = None

    else:
        payment = Payment(
            registration_id=registration.id,
            amount=workshop.price,
            status="PENDING",
            stripe_session_id=session.id
        )

        db.add(payment)

    db.commit()

    return {
        "checkout_url": session.url
    }


# Stripe Webhook

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.body()

    signature = request.headers.get(
        "stripe-signature"
    )

    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature"
        )

    # Verify Stripe webhook

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            settings.STRIPE_WEBHOOK_SECRET
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload"
        )

    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Stripe signature"
        )

    # Successful Checkout

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        # Check actual Stripe payment status

        if session.get("payment_status") != "paid":
            return {
                "status": "success"
            }

        registration_id = (
            session.get("metadata", {})
            .get("registration_id")
        )

        if not registration_id:
            return {
                "status": "success"
            }

        registration = (
            db.query(Registration)
            .filter(
                Registration.id == int(registration_id)
            )
            .first()
        )

        if registration is None:
            return {
                "status": "success"
            }

        payment = (
            db.query(Payment)
            .filter(
                Payment.registration_id == registration.id
            )
            .first()
        )

        if payment is None:
            return {
                "status": "success"
            }

        # Check whether payment was already successful

        already_successful = (
            payment.status == "SUCCESS"
        )

        # Update payment

        payment.status = "SUCCESS"

        payment.stripe_session_id = session.get(
            "id"
        )

        payment.stripe_payment_intent = session.get(
            "payment_intent"
        )

        # Confirm registration only after
        # successful Stripe payment

        registration.status = "CONFIRMED"

        db.commit()

        # Send confirmation email only once

        if not already_successful:

            participant = registration.user
            workshop = registration.workshop

            workshop_datetime = (
                f"{workshop.date} "
                f"{workshop.start_time}"
            )

            try:
                send_payment_confirmation_email(
                    participant_email=participant.email,
                    participant_name=participant.full_name,
                    workshop_name=workshop.title,
                    workshop_datetime=workshop_datetime,
                    registration_id=registration.id,
                    payment_status="SUCCESS"
                )

            except Exception:
                pass

    return {
        "status": "success"
    }