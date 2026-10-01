from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.patient import PatientCreate, PatientUpdate


# Create Patient
def create_patient(db: Session, patient_data: PatientCreate):
    patient = Patient(**patient_data.model_dump())

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


# Get All Patients (Admin)
def get_all_patients(db: Session):
    return db.query(Patient).all()


# Get Patient by ID
def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return patient


# Update Patient
def update_patient(
    db: Session,
    patient_id: int,
    patient_data: PatientUpdate
):
    patient = get_patient_by_id(db, patient_id)

    update_data = patient_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient


# Delete Patient
def delete_patient(db: Session, patient_id: int):
    patient = get_patient_by_id(db, patient_id)

    db.delete(patient)
    db.commit()

    return {"message": "Patient deleted successfully"}


# Get Patients Assigned to Doctor
def get_patients_by_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    return doctor.patients