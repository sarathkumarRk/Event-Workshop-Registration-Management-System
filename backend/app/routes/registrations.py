from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependency import (
    participant_required,
    get_current_user,
)
from app.models.user import User
from app.models.workshop import Workshop
from app.models.registration import Registration
from app.schemas.registration import (
    RegistrationCreate,
    RegistrationResponse,
    RegistrationListResponse,
)
from app.services.email_service import send_cancellation_email


router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)


# Register for Workshop - Participant Only

@router.post(
    "",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_registration(
    registration_data: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(participant_required)
):
    # Check workshop

    workshop = (
        db.query(Workshop)
        .filter(
            Workshop.id == registration_data.workshop_id
        )
        .first()
    )

    if workshop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found"
        )

    # Check duplicate registration

    existing_registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == current_user.id,
            Registration.workshop_id == workshop.id
        )
        .first()
    )

    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this workshop"
        )

    # Check workshop capacity

    if workshop.available_seats <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workshop is full"
        )

    # Check workshop started

    workshop_start = datetime.combine(
        workshop.date,
        workshop.start_time
    )

    if datetime.now() >= workshop_start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is not allowed after workshop has started"
        )

    # Create registration

    registration = Registration(
        user_id=current_user.id,
        workshop_id=workshop.id,
        status="PENDING"
    )

    # Reserve one seat

    workshop.available_seats -= 1

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration


# View Registrations - Participant + Admin
# Pagination

@router.get(
    "",
    response_model=RegistrationListResponse
)
def get_registrations(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0"
        )

    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be greater than 0"
        )

    query = db.query(Registration)

    # Participant can see only own registrations

    if current_user.role == "participant":
        query = query.filter(
            Registration.user_id == current_user.id
        )

    # Admin can see all registrations

    total = query.count()

    total_pages = (
        (total + limit - 1) // limit
        if total > 0
        else 0
    )

    offset = (page - 1) * limit

    registrations = (
        query
        .order_by(
            Registration.registered_at.desc()
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": registrations,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }


# View Registration Details
# Participant: Own Only
# Admin: Any Registration

@router.get(
    "/{registration_id}",
    response_model=RegistrationResponse
)
def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    # Participant can access only own registration

    if (
        current_user.role == "participant"
        and registration.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own registration"
        )

    return registration


# Cancel Registration

@router.delete(
    "/{registration_id}",
    response_model=RegistrationResponse
)
def cancel_registration(
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

    # Participant can cancel only own registration

    if registration.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own registration"
        )

    # Already cancelled

    if registration.status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is already cancelled"
        )

    workshop = (
        db.query(Workshop)
        .filter(
            Workshop.id == registration.workshop_id
        )
        .first()
    )

    # Cancel registration

    registration.status = "CANCELLED"
    registration.cancelled_at = datetime.utcnow()

    # Increase available seats

    if workshop:
        workshop.available_seats += 1

        if workshop.available_seats > workshop.capacity:
            workshop.available_seats = workshop.capacity

    db.commit()
    db.refresh(registration)

    # Send cancellation email

    if workshop:
        try:
            send_cancellation_email(
                participant_email=current_user.email,
                participant_name=current_user.full_name,
                workshop_name=workshop.title,
                registration_id=registration.id
            )
        except Exception:
            pass

    return registration