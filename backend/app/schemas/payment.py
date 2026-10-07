from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentResponse(BaseModel):
    id: int
    registration_id: int
    amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CheckoutSessionResponse(BaseModel):
    checkout_url: str