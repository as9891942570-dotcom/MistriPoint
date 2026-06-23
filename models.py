from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Numeric, Text

from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    mobile = Column(String(15), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class WorkerProfile(Base):
    __tablename__ = "worker_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)

    name = Column(String(100))
    mobile = Column(String(15))
    email = Column(String(100))

    gender = Column(String(20))
    date_of_birth = Column(Date)

    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pin_code = Column(String(10))

    skill = Column(String(100))
    experience = Column(Integer)

    salary = Column(Numeric(10, 2))

    joining_date = Column(Date)

    status = Column(String(20))

    aadhaar_number = Column(String(20))
    pan_number = Column(String(20))

    profile_photo = Column(Text)