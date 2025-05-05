import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class ScheduleType(str, PyEnum):
    date = "date"
    interval = "interval"
    cron = "cron"


class UserScanSchedule(Base):
    __tablename__ = "user_scan_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_type = Column(Enum(ScheduleType), nullable=False)
    user_scan_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    # Date trigger
    run_date = Column(DateTime(timezone=True), nullable=True)

    # Interval trigger
    interval_seconds = Column(Integer, nullable=True)
    interval_minutes = Column(Integer, nullable=True)
    interval_hours = Column(Integer, nullable=True)

    # Cron trigger
    cron_second = Column(String, nullable=True)
    cron_minute = Column(String, nullable=True)
    cron_hour = Column(String, nullable=True)
    cron_day = Column(String, nullable=True)
    cron_month = Column(String, nullable=True)
    cron_day_of_week = Column(String, nullable=True)

    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
