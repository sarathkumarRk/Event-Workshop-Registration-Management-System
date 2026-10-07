from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    registration_id = Column(
        Integer,
        ForeignKey("registrations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    status = Column(
        Enum("PENDING", "SUCCESS", "FAILED", "REFUNDED"),
        nullable=False,
        default="PENDING"
    )

    stripe_session_id = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )

    stripe_payment_intent = Column(
        String(255),
        unique=True,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    registration = relationship(
        "Registration",
        back_populates="payment"
    )