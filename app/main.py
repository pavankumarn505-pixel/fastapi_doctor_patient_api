from pathlib import Path
from dotenv import load_dotenv

# Load environment variables before importing other app modules
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

from fastapi import FastAPI

from app.database import Base, engine

# Import models before creating database tables
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
import app.models.assignment

# Import routers
from app.routers.auth import router as auth_router
from app.routers.doctors import router as doctors_router
from app.routers.patients import router as patients_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Doctor Patient API",
    description="End-to-End Backend Application for managing Doctors and Patients",
    version="1.0.0"
)

# Register API routers
app.include_router(auth_router)
app.include_router(doctors_router)
app.include_router(patients_router)


@app.get("/")
def home():
    return {
        "message": "Doctor Patient API is working"
    }