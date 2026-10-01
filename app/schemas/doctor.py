from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)