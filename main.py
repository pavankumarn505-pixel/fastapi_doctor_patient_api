from typing import List
 
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, EmailStr, Field
 
 
# Create FastAPI application

app = FastAPI(

    title="Doctor and Patient Management API",

    description="REST API to manage doctors and patients",

    version="1.0.0"

)
 
 
# -----------------------------

# Pydantic Models

# -----------------------------
 
class Doctor(BaseModel):

    id: int | None = None

    name: str

    specialization: str

    email: EmailStr

    is_active: bool = True
 
 
class Patient(BaseModel):

    name: str

    age: int = Field(gt=0)

    phone: str
 
 
# -----------------------------

# In-memory storage

# -----------------------------
 
doctors: List[Doctor] = []

patients: List[Patient] = []
 
 
# -----------------------------

# Doctor APIs

# -----------------------------
 
@app.post("/doctors", response_model=Doctor)

def create_doctor(doctor: Doctor):

    doctor.id = len(doctors) + 1

    doctors.append(doctor)

    return doctor
 
 
@app.get("/doctors", response_model=List[Doctor])

def get_doctors():

    return doctors
 
 
@app.get("/doctors/{doctor_id}", response_model=Doctor)

def get_doctor(doctor_id: int):
 
    for doctor in doctors:

        if doctor.id == doctor_id:

            return doctor
 
    raise HTTPException(

        status_code=404,

        detail="Doctor not found"

    )
 
 
# -----------------------------

# Patient APIs

# -----------------------------
 
@app.post("/patients", response_model=Patient)

def create_patient(patient: Patient):

    patients.append(patient)

    return patient
 
 
@app.get("/patients", response_model=List[Patient])

def get_patients():

    return patients
 