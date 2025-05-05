# scripts/create_tables.py
from app.models.base import Base
from app.db.session import engine

def create_all():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all()