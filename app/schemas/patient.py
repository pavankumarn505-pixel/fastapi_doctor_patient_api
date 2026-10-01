from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# Schema for creating a patient
class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0)
    phone: str = Field(..., pattern=r"^\d{10,15}$")


# Schema for updating a patient
class PatientUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=2, max_length=100
    )
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = Field(
        default=None, pattern=r"^\d{10,15}$"
    )


# Schema for returning patient details
class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str

    model_config = ConfigDict(from_attributes=True)