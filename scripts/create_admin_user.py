# scripts/create_admin_user.py

from sqlalchemy.orm import Session

from app.core.security.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User
import uuid
#even not used here, still need import
from app.models import user, organization

def create_default_admin():
    db: Session = SessionLocal()

    admin_email = "admin@example.com"
    existing = db.query(User).filter(User.email == admin_email).first()

    if not existing:
        user = User(
            id=uuid.uuid4(),
            email=admin_email,
            hashed_password=hash_password("admin123"),
            role="admin",
            organization_id="c8497b18-ac88-49a9-ab84-c6f3ce2c87cf"
        )
        db.add(user)
        db.commit()
        print("Admin user created.")
    else:
        print("Admin already exists.")

if __name__ == "__main__":
    create_default_admin()