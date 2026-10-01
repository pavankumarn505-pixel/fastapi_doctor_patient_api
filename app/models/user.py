from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="doctor", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    doctor = relationship(
        "Doctor",
        back_populates="user",
        uselist=False
    )