# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import SessionLocal
from app.repositories.unit_of_work import UnitOfWork
from app.routers import auth_router, users_router, organization_router, user_scan_router, user_scan_result_router
from app.services.scheduler_service import ScheduleService

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        uow = UnitOfWork(db)
        schedule_service = ScheduleService()
        schedule_service.load_schedules_from_db(uow)
        print("✅ Loaded scheduled jobs from DB")
        yield  # ✅ MUST have this
    finally:
        db.close()
        print("🛑 Database connection closed")

app = FastAPI(
    title="Domain Vulnerability Scanner",
    description="SaaS app with multi-tenant architecture, scanning, and AI reporting",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users_router.router, prefix="/api/users", tags=["Users"])
app.include_router(organization_router.router, prefix="/api/orgs", tags=["Organizations"])
app.include_router(user_scan_router.router, prefix="/api/scan", tags=["Scan"])
app.include_router(user_scan_result_router.router, prefix="/api/scan_results", tags=["Scan"])


# Health Check Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Domain Scanner API"}
