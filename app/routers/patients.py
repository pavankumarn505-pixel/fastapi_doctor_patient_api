from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.patient import PatientCreate, PatientResponse
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# Create Patient (Admin only)
@router.post("/", response_model=PatientResponse,
             status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    new_patient = Patient(**patient.model_dump())

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# Get All Patients
@router.get("/", response_model=list[PatientResponse])
def get_patients(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(Patient).all()

    if current_user.role == "doctor":
        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user.id,
            Doctor.is_active == True
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor profile not found"
            )

        return doctor.patients

    raise HTTPException(
        status_code=403,
        detail="Access denied"
    )


# Get Patient by ID
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Admin can view any patient
    if current_user.role == "admin":
        return patient

    # Doctor can view only assigned patients
    if current_user.role == "doctor":
        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user.id,
            Doctor.is_active == True
        ).first()

        if not doctor or patient not in doctor.patients:
            raise HTTPException(
                status_code=403,
                detail="You can only view your assigned patients"
            )

        return patient

    raise HTTPException(
        status_code=403,
        detail="Access denied"
    )