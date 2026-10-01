from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from app.schemas.patient import PatientResponse
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# Create Doctor (Admin only)
@router.post("/", response_model=DoctorResponse,
             status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    new_doctor = Doctor(**doctor.model_dump())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


# List Doctors (Authenticated users)
@router.get("/", response_model=list[DoctorResponse])
def get_doctors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Doctor).filter(
        Doctor.is_active == True
    ).all()


# Get Doctor by ID
@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


# Update Doctor (Admin only)
@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    update_data = doctor_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = db.query(Doctor).filter(
            Doctor.email == update_data["email"],
            Doctor.id != doctor_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )

    for key, value in update_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor


# Soft Delete Doctor (Admin only)
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False
    db.commit()

    return {"message": "Doctor deactivated successfully"}


# Assign Patient to Doctor (Admin only)
@router.post("/{doctor_id}/patients/{patient_id}")
def assign_patient(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if patient in doctor.patients:
        raise HTTPException(
            status_code=400,
            detail="Patient already assigned to this doctor"
        )

    doctor.patients.append(patient)
    db.commit()

    return {"message": "Patient assigned successfully"}


# Get Doctor's Assigned Patients
@router.get("/{doctor_id}/patients",
            response_model=list[PatientResponse])
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if current_user.role == "doctor" and current_user.id != doctor.user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own patients"
        )

    return doctor.patients