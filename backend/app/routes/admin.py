from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependency import admin_required
from app.models.user import User
from app.models.workshop import Workshop
from app.models.registration import Registration
from app.models.payment import Payment


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# Admin Dashboard

@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    total_workshops = (
        db.query(Workshop)
        .count()
    )

    total_registrations = (
        db.query(Registration)
        .count()
    )

    confirmed_registrations = (
        db.query(Registration)
        .filter(
            Registration.status == "CONFIRMED"
        )
        .count()
    )

    cancelled_registrations = (
        db.query(Registration)
        .filter(
            Registration.status == "CANCELLED"
        )
        .count()
    )

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(Payment.amount),
                0
            )
        )
        .filter(
            Payment.status == "SUCCESS"
        )
        .scalar()
    )

    return {
        "total_workshops": total_workshops,
        "total_registrations": total_registrations,
        "confirmed_registrations": confirmed_registrations,
        "cancelled_registrations": cancelled_registrations,
        "total_revenue": total_revenue
    }


# View Participants

@router.get("/participants")
def get_participants(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    participants = (
        db.query(User)
        .filter(
            User.role == "participant"
        )
        .all()
    )

    return participants


# View Payments

@router.get("/payments")
def get_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    payments = (
        db.query(Payment)
        .order_by(
            Payment.created_at.desc()
        )
        .all()
    )

    return payments


# View Revenue

@router.get("/revenue")
def get_revenue(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(Payment.amount),
                0
            )
        )
        .filter(
            Payment.status == "SUCCESS"
        )
        .scalar()
    )

    return {
        "total_revenue": total_revenue
    }