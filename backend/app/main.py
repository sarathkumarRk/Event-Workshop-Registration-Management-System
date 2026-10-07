from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models

from app.routes.auth import router as auth_router
from app.routes.workshops import router as workshop_router
from app.routes.registrations import router as registration_router
from app.routes.payments import router as payment_router
from app.routes.admin import router as admin_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Event Workshop Registration & Management System",
)


# Frontend Connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routes
app.include_router(auth_router)
app.include_router(workshop_router)
app.include_router(registration_router)
app.include_router(payment_router)
app.include_router(admin_router)


# Root API
@app.get("/")
def root():
    return {
        "message": "Event Workshop Registration & Management System API"
    }