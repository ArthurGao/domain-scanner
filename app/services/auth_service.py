# app/services/auth_service.py
from fastapi import HTTPException

from app.core.security.security import create_access_token, verify_password
from app.repositories.unit_of_work import UnitOfWork
from app.services import user_service
from app.schemas.auth_schema import LoginRequest, TokenResponse


def authenticate_user(login_data: LoginRequest, uow: UnitOfWork) -> TokenResponse:
    user = user_service.get_user_by_email(login_data.email, uow)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return TokenResponse(access_token=token, token_type="bearer")
