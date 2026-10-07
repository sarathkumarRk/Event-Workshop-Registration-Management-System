from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RegistrationCreate(BaseModel):
    workshop_id: int


class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    workshop_id: int
    status: str
    registered_at: datetime
    cancelled_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class RegistrationListResponse(BaseModel):
    items: list[RegistrationResponse]
    page: int
    limit: int
    total: int
    total_pages: int