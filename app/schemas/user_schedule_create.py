from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.user_scan_schedules import ScheduleType

class ScheduleCreate(BaseModel):
    schedule_type: ScheduleType
    user_scan_id: UUID
    id: UUID
    name: str
    # Date trigger
    run_date: Optional[datetime] = None

    # Interval trigger
    interval_seconds: Optional[int] = None
    interval_minutes: Optional[int] = None
    interval_hours: Optional[int] = None

    # Cron trigger
    cron_second: Optional[str] = None
    cron_minute: Optional[str] = None
    cron_hour: Optional[str] = None
    cron_day: Optional[str] = None
    cron_month: Optional[str] = None
    cron_day_of_week: Optional[str] = None

    enabled: bool = True

    model_config = {
        "from_attributes": True
    }