from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.user_scan import ScanType, ScanStatus
from app.models.user_scan_schedules import ScheduleType

class ScheduleSettings(BaseModel):
    schedule_type: ScheduleType
    run_date: Optional[datetime] = None
    interval_seconds: Optional[int] = None
    interval_minutes: Optional[int] = None
    interval_hours: Optional[int] = None
    cron_second: Optional[str] = None
    cron_minute: Optional[str] = None
    cron_hour: Optional[str] = None
    cron_day: Optional[str] = None
    cron_month: Optional[str] = None
    cron_day_of_week: Optional[str] = None
    enabled: bool = True

class ScanCreate(BaseModel):
    type: ScanType = ScanType.immediate
    name: str
    schedule: Optional[ScheduleSettings] = None

class UserScanResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    type: ScanType
    created_at: datetime
    status: ScanStatus

    class Config:
        from_attributes = True