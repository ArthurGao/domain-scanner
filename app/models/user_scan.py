import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base

class ScanStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class ScanType(str, enum.Enum):
    immediate = "immediate"
    scheduled = "scheduled"

class UserScan(Base):
    __tablename__ = "user_scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    type = Column(Enum(ScanType), default=ScanType.immediate)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(ScanStatus), default=ScanStatus.pending)
    results = relationship("UserScanResult", back_populates="scan", cascade="all, delete-orphan")


