from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

doctor_patient = Table(
    "doctor_patient",
    Base.metadata,
    Column(
        "doctor_id",
        Integer,
        ForeignKey("doctors.id"),
        primary_key=True
    ),
    Column(
        "patient_id",
        Integer,
        ForeignKey("patients.id"),
        primary_key=True
    )
)