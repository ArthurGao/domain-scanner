from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List

from app.schemas.user_scan_result_schema import ScanResultCreate, ScanResultResponse
from app.services.user_scan_result_service import UserScanResultService
from app.repositories.unit_of_work import UnitOfWork, get_uow
from app.core.security.permission import get_current_user
from app.models.user import User

router = APIRouter()
scan_result_service = UserScanResultService()


@router.post("/", response_model=ScanResultResponse)
def create_scan_result(
        result_in: ScanResultCreate,
        uow: UnitOfWork = Depends(get_uow),
        current_user: User = Depends(get_current_user)
):
    return scan_result_service.create_result(result_in, uow)


@router.get("/{result_id}", response_model=ScanResultResponse)
def get_scan_result_by_id(
        result_id: UUID,
        uow: UnitOfWork = Depends(get_uow),
        current_user: User = Depends(get_current_user)
):
    result = scan_result_service.get_by_id(result_id, uow)
    if not result:
        raise HTTPException(status_code=404, detail="Scan result not found")
    if result.scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this result")
    return result


@router.get("/", response_model=List[ScanResultResponse])
def get_my_scan_results(
        uow: UnitOfWork = Depends(get_uow),
        current_user: User = Depends(get_current_user)
):
    return scan_result_service.get_by_user_id(current_user.id, uow)
