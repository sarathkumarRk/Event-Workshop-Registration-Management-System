from datetime import date, datetime, time

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Text,
    Time,
    Numeric,
    Enum,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    speaker = Column(String(150), nullable=False)

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    price = Column(Numeric(10, 2), nullable=False, default=0)
    capacity = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)

    status = Column(
        Enum("UPCOMING", "ONGOING", "COMPLETED", "CANCELLED"),
        nullable=False,
        default="UPCOMING"
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    registrations = relationship(
        "Registration",
        back_populates="workshop",
        cascade="all, delete-orphan"
    )