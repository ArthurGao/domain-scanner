# app/services/user_scan_result_service.py
from uuid import UUID, uuid4
from datetime import datetime, timezone

from typing import List, Optional

from app.models.user_scan_result import UserScanResult
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.user_scan_result_schema import ScanResultCreate


class UserScanResultService:
    def create_result(self, result_in: ScanResultCreate, uow: UnitOfWork) -> UserScanResult:
        result = UserScanResult(
            id=uuid4(),
            scan_id=result_in.scan_id,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
            status= result_in.status
        )
        return uow.user_scan_result_repo.create(result)

    def get_by_id(self, result_id: UUID, uow: UnitOfWork) -> Optional[UserScanResult]:
        return uow.user_scan_result_repo.get_by_id(result_id)

    def get_by_user_id(self, user_id: UUID, uow: UnitOfWork) -> List[UserScanResult]:
        return uow.user_scan_result_repo.get_by_user_id(user_id)