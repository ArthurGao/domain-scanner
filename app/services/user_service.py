# app/services/user_service.py
from app.core.security.security import hash_password
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.user_schema import UserCreate
from app.models.user import User
from fastapi import HTTPException, status


def register_user(user_in: UserCreate, uow: UnitOfWork, current_user: User) -> User:
    if str(current_user.organization_id) != str(user_in.organization_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create user in this organization"
        )

    existing = uow.user_repo.get_by_email(user_in.email)
    if existing:
        raise ValueError("User already exists")

    user = User(
        email=str(user_in.email),
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
        organization_id=user_in.organization_id
    )
    uow.user_repo.save(user)
    uow.commit()
    return user


def get_user_by_id(user_id: str, uow: UnitOfWork) -> User | None:
    return uow.user_repo.get_by_id(user_id)


def get_user_by_email(email: str, uow: UnitOfWork) -> User | None:
    return uow.user_repo.get_by_email(email)
