# app/repositories/organization_repository.py
from sqlalchemy.orm import Session
from app.models.organization import Organization

class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Organization | None:
        return self.db.query(Organization).filter(Organization.name == name).first()

    def save(self, org: Organization) -> Organization:
        self.db.add(org)
        self.db.flush()
        return org