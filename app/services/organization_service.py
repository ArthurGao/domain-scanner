# app/services/organization_service.py
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.organization_schema import OrgCreate
from app.models.organization import Organization

def create_organization(org_in: OrgCreate, uow: UnitOfWork) -> Organization:
    existing = uow.organization_repo.get_by_name(org_in.name)
    if existing:
        raise ValueError("Organization name already exists")

    org = Organization(name=org_in.name)
    saved = uow.organization_repo.save(org)
    uow.commit()
    return saved