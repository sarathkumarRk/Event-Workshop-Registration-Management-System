from datetime import date as date_type
from datetime import datetime, time as time_type
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WorkshopCreate(BaseModel):
    title: str
    description: str
    speaker: str
    date: date_type
    start_time: time_type
    end_time: time_type
    price: Decimal = Field(ge=0)
    capacity: int = Field(gt=0)


class WorkshopUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    speaker: str | None = None
    date: date_type | None = None
    start_time: time_type | None = None
    end_time: time_type | None = None
    price: Decimal | None = Field(
        default=None,
        ge=0
    )
    capacity: int | None = Field(
        default=None,
        gt=0
    )
    status: str | None = None


class WorkshopResponse(BaseModel):
    id: int
    title: str
    description: str
    speaker: str
    date: date_type
    start_time: time_type
    end_time: time_type
    price: Decimal
    capacity: int
    available_seats: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class WorkshopListResponse(BaseModel):
    items: list[WorkshopResponse]
    page: int
    limit: int
    total: int
    total_pages: int