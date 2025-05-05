from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.core.security.permission import get_current_user
from app.models.user import User
from app.repositories.unit_of_work import UnitOfWork, get_uow
from app.schemas.user_scan_schema import ScanCreate, UserScanResponse
from app.services.scheduler_service import ScheduleService
from app.services.user_scan_service import UserScanService

router = APIRouter()
scan_service = UserScanService(schedule_service=ScheduleService())

@router.post("/", response_model=UserScanResponse)
def create_scan(
    scan_in: ScanCreate,
    uow: UnitOfWork = Depends(get_uow),
    current_user: User = Depends(get_current_user)
):
    scan = scan_service.create_scan(scan_in, uow, current_user)
    if not scan:
        raise HTTPException(status_code=400, detail="Scan creation failed")
    return scan


@router.get("/", response_model=List[UserScanResponse])
def get_my_scans(
    uow: UnitOfWork = Depends(get_uow),
    current_user: User = Depends(get_current_user)
):
    return scan_service.get_by_user_id(current_user.id, uow)


@router.get("/{scan_id}", response_model=UserScanResponse)
def get_scan_by_id(
    scan_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    current_user: User = Depends(get_current_user)
):
    scan = scan_service.get_by_id(scan_id, uow)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to view this scan")
    return scan

