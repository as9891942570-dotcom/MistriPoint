from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, Text, Float, ForeignKey, Time,DateTime

from sqlalchemy.sql import func
from database import Base
from datetime import datetime

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
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_available = Column(Boolean, default=True)
    working_radius = Column(Integer)
    preferred_area = Column(String(255))

    profile_image = Column(Text)
    aadhaar_front = Column(Text)
    aadhaar_back = Column(Text)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), unique=True, nullable=False)


class WorkerSkill(Base):
    __tablename__ = "worker_skills"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))



class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer)

    title = Column(String(150), nullable=False)
    description = Column(Text)

    category_id = Column(Integer, nullable=False)

    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))

    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))

    budget = Column(Numeric(10, 2))

    job_date = Column(Date)
    job_time = Column(Time)

    status = Column(String(20), default="Open")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

class WorkerKYC(Base):

    __tablename__ = "worker_kyc"

    id = Column(Integer, primary_key=True, index=True)

    worker_id = Column(
        Integer,
        ForeignKey("workers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    aadhaar_number = Column(
        String(12),
        unique=True,
        nullable=False
    )

    pan_number = Column(String(10))

    account_holder_name = Column(String(100))

    bank_name = Column(String(100))

    account_number = Column(String(30))

    ifsc_code = Column(String(15))

    aadhaar_front = Column(String(255))

    aadhaar_back = Column(String(255))

    pan_card_image = Column(String(255))

    passbook_image = Column(String(255))

    selfie_image = Column(String(255))

    kyc_status = Column(
        String(20),
        default="Pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class JobApplication(Base):

    __tablename__ = "job_applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    worker_id = Column(
        Integer,
        ForeignKey("workers.id", ondelete="CASCADE"),
        nullable=False
    )

    message = Column(Text)

    expected_price = Column(
        Numeric(10,2)
    )

    status = Column(
        String(20),
        default="Pending"
    )

    applied_at = Column(
        DateTime,
        default=datetime.utcnow
    )