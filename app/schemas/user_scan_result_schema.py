from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ScanResultCreate(BaseModel):
    scan_id: UUID
    result: str | None = None

class ScanResultResponse(BaseModel):
    id: UUID
    scan_id: UUID
    started_at: datetime
    completed_at: datetime | None = None
    result: str | None = None

    class Config:
        from_attributes = True