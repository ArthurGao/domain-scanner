from typing import List

from sqlalchemy.orm import Session

from app.models.user_scan_schedules import UserScanSchedule


class ScheduleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, schedule: UserScanSchedule):
        self.db.add(schedule)

    def get_all_enabled(self) -> List[UserScanSchedule]:
        return (
            self.db.query(UserScanSchedule)
            .filter(UserScanSchedule.enabled == True)
            .all()
        )
