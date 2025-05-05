import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.user_scan import ScanStatus

class UserScanResult(Base):
    __tablename__ = "user_scan_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("user_scans.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(Enum(ScanStatus), default=ScanStatus.pending)
    result = Column(String, nullable=True)
    scan = relationship("UserScan", back_populates="results")