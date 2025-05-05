# app/repositories/user_repository.py
from sqlalchemy.orm import Session
from app.models.user import User
from uuid import UUID

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user