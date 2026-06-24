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

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    mobile = Column(String(15))

    gender = Column(String(20))
    date_of_birth = Column(Date)

    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))

    category_id = Column(Integer)

    experience_years = Column(Integer)

    skills = Column(Text)

    about = Column(Text)

    aadhaar_number = Column(String(20))

    status = Column(String(20))

    profile_image = Column(Text)
    aadhaar_front = Column(Text)
    aadhaar_back = Column(Text)