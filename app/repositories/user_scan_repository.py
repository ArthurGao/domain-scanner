from typing import List, Optional, cast
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user_scan import UserScan


class UserScanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, scan: UserScan) -> UserScan:
        self.db.add(scan)
        self.db.flush()
        return scan

    def get_by_id(self, scan_id: UUID) -> Optional[UserScan]:
        return self.db.query(UserScan).filter(UserScan.id == scan_id).first()

    def get_by_user_id(self, user_id: UUID) -> List[UserScan]:
        scans: List[UserScan] = cast(List[UserScan], self.db.query(UserScan).filter(UserScan.user_id == user_id).all())
        return scans
