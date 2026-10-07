from math import ceil

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependency import get_current_user, admin_required
from app.models.user import User
from app.models.workshop import Workshop
from app.schemas.workshop import (
    WorkshopCreate,
    WorkshopUpdate,
    WorkshopResponse,
    WorkshopListResponse,
)


router = APIRouter(
    prefix="/workshops",
    tags=["Workshops"]
)


# Create Workshop - Admin Only

@router.post(
    "",
    response_model=WorkshopResponse,
    status_code=status.HTTP_201_CREATED
)
def create_workshop(
    workshop_data: WorkshopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    workshop = Workshop(
        title=workshop_data.title,
        description=workshop_data.description,
        speaker=workshop_data.speaker,
        date=workshop_data.date,
        start_time=workshop_data.start_time,
        end_time=workshop_data.end_time,
        price=workshop_data.price,
        capacity=workshop_data.capacity,
        available_seats=workshop_data.capacity,
        status="UPCOMING"
    )

    db.add(workshop)
    db.commit()
    db.refresh(workshop)

    return workshop


# View / Search / Pagination - Participant + Admin

@router.get(
    "",
    response_model=WorkshopListResponse
)
def get_workshops(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
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

    query = db.query(Workshop)

    # Search by workshop title
    if search:
        query = query.filter(
            Workshop.title.ilike(f"%{search}%")
        )

    total = query.count()

    total_pages = ceil(total / limit) if total > 0 else 0

    offset = (page - 1) * limit

    workshops = (
        query
        .order_by(
            Workshop.date,
            Workshop.start_time
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": workshops,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }


# View Single Workshop - Participant + Admin

@router.get(
    "/{workshop_id}",
    response_model=WorkshopResponse
)
def get_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workshop = (
        db.query(Workshop)
        .filter(Workshop.id == workshop_id)
        .first()
    )

    if workshop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found"
        )

    return workshop


# Update Workshop - Admin Only

@router.put(
    "/{workshop_id}",
    response_model=WorkshopResponse
)
def update_workshop(
    workshop_id: int,
    workshop_data: WorkshopUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    workshop = (
        db.query(Workshop)
        .filter(Workshop.id == workshop_id)
        .first()
    )

    if workshop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found"
        )

    update_data = workshop_data.model_dump(
        exclude_unset=True
    )

    # Handle capacity update

    if "capacity" in update_data:

        current_registered = (
            workshop.capacity - workshop.available_seats
        )

        new_capacity = update_data["capacity"]

        if new_capacity < current_registered:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Capacity cannot be less than "
                    "current registered participants"
                )
            )

        update_data["available_seats"] = (
            new_capacity - current_registered
        )

    # Update workshop fields

    for key, value in update_data.items():
        setattr(workshop, key, value)

    db.commit()
    db.refresh(workshop)

    return workshop


# Delete Workshop - Admin Only

@router.delete(
    "/{workshop_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    workshop = (
        db.query(Workshop)
        .filter(Workshop.id == workshop_id)
        .first()
    )

    if workshop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found"
        )

    db.delete(workshop)
    db.commit()

    return None