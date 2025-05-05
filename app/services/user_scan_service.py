import uuid
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from app.models.user import User
from app.models.user_scan import UserScan
from app.models.user_scan_schedules import UserScanSchedule
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.user_scan_schema import ScanCreate
from app.schemas.user_schedule_create import ScheduleCreate
from app.services.scheduler_service import ScheduleService


class UserScanService:

    def __init__(self, schedule_service: ScheduleService):
        self.schedule_service = schedule_service

    def create_scan(self, scan_in: ScanCreate, uow: UnitOfWork, current_user: User) -> UserScan:
        scan = UserScan(
            id=uuid.uuid4(),
            user_id=current_user.id,
            type=scan_in.type,
            created_at=datetime.utcnow(),
            name=scan_in.name,
        )
        uow.user_scan_repo.create(scan)

        if scan_in.type == "scheduled" and scan_in.schedule:
            schedule_model = UserScanSchedule(
                id=uuid.uuid4(),
                name=scan_in.name,
                schedule_type=scan_in.schedule.schedule_type,
                run_date=scan_in.schedule.run_date,
                interval_seconds=scan_in.schedule.interval_seconds,
                interval_minutes=scan_in.schedule.interval_minutes,
                interval_hours=scan_in.schedule.interval_hours,
                cron_second=scan_in.schedule.cron_second,
                cron_minute=scan_in.schedule.cron_minute,
                cron_hour=scan_in.schedule.cron_hour,
                cron_day=scan_in.schedule.cron_day,
                cron_month=scan_in.schedule.cron_month,
                cron_day_of_week=scan_in.schedule.cron_day_of_week,
                enabled=scan_in.schedule.enabled,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                user_scan_id=scan.id
            )
            uow.schedule_repo.create(schedule_model)
            schedule_schema = ScheduleCreate.model_validate(schedule_model)
            self.schedule_service.start_scheduler(schedule_schema)

        uow.commit()
        return scan


    def get_by_id(self, scan_id: UUID, uow: UnitOfWork) -> Optional[UserScan]:
        return uow.user_scan_repo.get_by_id(scan_id)

    def get_by_user_id(self, user_id: UUID, uow: UnitOfWork) -> List[UserScan]:
        return uow.user_scan_repo.get_by_user_id(user_id)