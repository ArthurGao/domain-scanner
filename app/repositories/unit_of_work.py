# app/uow/unit_of_work.py
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_scan_repository import UserScanRepository
from app.repositories.user_scan_result_repository import UserScanResultRepository


class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db
        self.organization_repo = OrganizationRepository(db)
        self.user_repo = UserRepository(db)
        self.user_scan_repo = UserScanRepository(db)
        self.user_scan_result_repo = UserScanResultRepository(db)
        self.schedule_repo = ScheduleRepository(db)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

def get_uow(db: Session = Depends(get_db)) -> UnitOfWork:
    return UnitOfWork(db)