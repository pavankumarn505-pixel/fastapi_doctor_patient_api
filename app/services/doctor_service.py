from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.doctor import DoctorCreate, DoctorUpdate


# Create Doctor
def create_doctor(db: Session, doctor_data: DoctorCreate):
    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor_data.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor email already exists"
        )

    doctor = Doctor(**doctor_data.model_dump())

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


# Get All Active Doctors
def get_all_doctors(db: Session):
    return db.query(Doctor).filter(
        Doctor.is_active == True
    ).all()


# Get Doctor by ID
def get_doctor_by_id(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    return doctor


# Update Doctor
def update_doctor(
    db: Session,
    doctor_id: int,
    doctor_data: DoctorUpdate
):
    doctor = get_doctor_by_id(db, doctor_id)

    update_data = doctor_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = db.query(Doctor).filter(
            Doctor.email == update_data["email"],
            Doctor.id != doctor_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )

    for key, value in update_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor


# Soft Delete Doctor
def delete_doctor(db: Session, doctor_id: int):
    doctor = get_doctor_by_id(db, doctor_id)

    doctor.is_active = False

    db.commit()

    return {
        "message": "Doctor deactivated successfully"
    }


# Assign Patient to Doctor
def assign_patient(
    db: Session,
    doctor_id: int,
    patient_id: int
):
    doctor = get_doctor_by_id(db, doctor_id)

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    if patient in doctor.patients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient already assigned to this doctor"
        )

    doctor.patients.append(patient)

    db.commit()

    return {
        "message": "Patient assigned successfully"
    }


# Get Doctor's Patients
def get_doctor_patients(db: Session, doctor_id: int):
    doctor = get_doctor_by_id(db, doctor_id)

    return doctor.patients