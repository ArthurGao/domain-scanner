# app/routers/users_router.py
from fastapi import APIRouter, Depends, HTTPException

from app.core.security.permission import get_current_user, admin_required
from app.repositories.unit_of_work import UnitOfWork, get_uow
from app.schemas.user_schema import UserCreate, UserResponse
from app.services import user_service

router = APIRouter()

@router.post("/", response_model=UserResponse)
def register_user(
    user_in: UserCreate,
    uow: UnitOfWork = Depends(get_uow),
    current_user = Depends(admin_required)
):
    try:
        return user_service.register_user(user_in, uow, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user