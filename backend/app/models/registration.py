from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    workshop_id = Column(
        Integer,
        ForeignKey("workshops.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    status = Column(
        Enum("PENDING", "CONFIRMED", "CANCELLED"),
        nullable=False,
        default="PENDING"
    )

    registered_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    cancelled_at = Column(
        DateTime,
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "workshop_id",
            name="uq_user_workshop"
        ),
    )

    user = relationship(
        "User",
        back_populates="registrations"
    )

    workshop = relationship(
        "Workshop",
        back_populates="registrations"
    )

    payment = relationship(
        "Payment",
        back_populates="registration",
        uselist=False,
        cascade="all, delete-orphan"
    )