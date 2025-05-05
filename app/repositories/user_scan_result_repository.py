from typing import List, Optional, cast
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user_scan_result import UserScanResult


class UserScanResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, result: UserScanResult) -> UserScanResult:
        self.db.add(result)
        self.db.flush()
        return result

    def get_by_id(self, result_id: UUID) -> Optional[UserScanResult]:
        return self.db.query(UserScanResult).filter(UserScanResult.id == result_id).first()

    def get_by_user_id(self, user_id: UUID) -> List[UserScanResult]:
        return (
            cast(List[UserScanResult], self.db.query(UserScanResult)
            .join(UserScanResult.scan)
            .filter(UserScanResult.scan.has(user_id=user_id))
            .all())
        )
