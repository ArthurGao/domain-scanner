# app/routers/auth_schema.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        uow = UnitOfWork(db)
        return auth_service.authenticate_user(login_data, uow)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

