# app/routers/organization_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security.permission import admin_required
from app.db.session import get_db
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.organization_schema import OrgCreate, OrgResponse
from app.services import organization_service

router = APIRouter()

@router.post("/", response_model=OrgResponse)
def create_org(org_in: OrgCreate, db: Session = Depends(get_db), _=Depends(admin_required)):
    try:
        uow = UnitOfWork(db)
        return organization_service.create_organization(org_in, uow)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))