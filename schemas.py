from pydantic import BaseModel
from datetime import date, time
from typing import List
from decimal import Decimal
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    mobile: str
    password: str

class LoginRequest(BaseModel):
    mobile: str
    password: str

class ChangePasswordRequest(BaseModel):
    mobile: str
    old_password: str
    new_password: str

class Labour(BaseModel):
    name: str
    mobile: str
    age: int
    skill: str


class WorkerCreate(BaseModel):
    name: str
    email: str
    mobile: str
    gender: str
    date_of_birth: date
    address: str
    city: str
    state: str
    pincode: str
    category_id: int
    experience_years: int
    skills: str
    about: str
    aadhaar_number: str
    latitude: float
    longitude: float
    is_available: bool
    profile_image: str
    aadhaar_front: str
    aadhaar_back: str

class WorkerLocation(BaseModel):
    latitude: float
    longitude: float
class WorkerAvailability(BaseModel):
    is_available: bool
class WorkerRadius(BaseModel):
    working_radius: int
class WorkerPreferredArea(BaseModel):
    preferred_area: str

class SkillCreate(BaseModel):
    skill_name: str


class WorkerSkillCreate(BaseModel):
    worker_id: int
    skill_ids: List[int]


class WorkerSkillUpdate(BaseModel):
    skill_ids: List[int]
class JobCreate(BaseModel):
    customer_id: int

    title: str
    description: Optional[str] = None

    category_id: int

    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None

    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

    budget: Decimal

    job_date: date
    job_time: time
class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    category_id: Optional[int] = None

    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None

    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

    budget: Optional[Decimal] = None

    job_date: Optional[date] = None
    job_time: Optional[time] = None

    status: Optional[str] = None
class JobResponse(BaseModel):
    id: int

    customer_id: int

    title: str
    description: Optional[str]

    category_id: int

    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]

    latitude: Optional[Decimal]
    longitude: Optional[Decimal]

    budget: Decimal

    job_date: date
    job_time: time

    status: str

    class Config:
        from_attributes = True
class WorkerStatusUpdate(BaseModel):
    status: str
class AdminWorkerUpdate(BaseModel):

    name: str
    email: str
    mobile: str

    gender: str
    date_of_birth: date

    address: str
    city: str
    state: str
    pincode: str

    category_id: int

    experience_years: int

    skills: str

    about: str

    aadhaar_number: str

    profile_image: str
    aadhaar_front: str
    aadhaar_back: str
class WorkerKYCCreate(BaseModel):

    worker_id: int

    aadhaar_number: str

    pan_number: Optional[str] = None

    account_holder_name: Optional[str] = None

    bank_name: Optional[str] = None

    account_number: Optional[str] = None

    ifsc_code: Optional[str] = None

    aadhaar_front: Optional[str] = None

    aadhaar_back: Optional[str] = None

    pan_card_image: Optional[str] = None

    passbook_image: Optional[str] = None

    selfie_image: Optional[str] = None
class WorkerKYCResponse(BaseModel):

    id: int

    worker_id: int

    aadhaar_number: str

    pan_number: Optional[str]

    account_holder_name: Optional[str]

    bank_name: Optional[str]

    account_number: Optional[str]

    ifsc_code: Optional[str]

    aadhaar_front: Optional[str]

    aadhaar_back: Optional[str]

    pan_card_image: Optional[str]

    passbook_image: Optional[str]

    selfie_image: Optional[str]

    kyc_status: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


class JobApplicationCreate(BaseModel):

    job_id: int

    worker_id: int

    message: Optional[str] = None

    expected_price: float


class JobApplicationResponse(BaseModel):

    id: int

    job_id: int

    worker_id: int

    message: Optional[str]

    expected_price: float

    status: str

    applied_at: datetime

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):

    job_application_id: int

    job_id: int

    worker_id: int

    booking_date: date

    booking_time: time

    address: str

    amount: float

class BookingResponse(BaseModel):

    id: int

    job_application_id: int

    job_id: int

    worker_id: int

    booking_date: date

    booking_time: time

    address: str

    amount: float

    payment_status: str

    booking_status: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True

class BookingStatusUpdate(BaseModel):

    booking_status: str