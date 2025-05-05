from sqlalchemy.orm import Session
from typing import Optional

from app.models.email import Email
from app.models.breach import Breach
from app.models.breach_email import BreachEmail


class EmailRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_emails(self):
        return self.db.query(Email).filter(Email.status == "active").all()

    def get_email_by_address(self, email: str) -> Optional[Email]:
        return self.db.query(Email).filter(Email.email == email, Email.status == "active").first()


class BreachRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Breach]:
        return self.db.query(Breach).filter(Breach.name == name).first()

    def create(self, breach: Breach):
        self.db.add(breach)
        self.db.flush()  # Get id without commit


class BreachEmailRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists(self, breach_id: str, email_id: str) -> bool:
        return self.db.query(BreachEmail).filter(
            BreachEmail.breaches_id == breach_id,
            BreachEmail.emails_id == email_id
        ).first() is not None

    def create(self, breach_id: str, email_id: str):
        breach_email = BreachEmail(breaches_id=breach_id, emails_id=email_id)
        self.db.add(breach_email)