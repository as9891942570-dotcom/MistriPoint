from pydantic import BaseModel
from typing import Optional
from datetime import date

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

class WorkerProfileSchema(BaseModel):
        user_id: int

        name: str
        mobile: str
        email: Optional[str] = None

        gender: Optional[str] = None
        date_of_birth: Optional[date] = None

        address: Optional[str] = None
        city: Optional[str] = None
        state: Optional[str] = None
        pin_code: Optional[str] = None

        skill: Optional[str] = None
        experience: Optional[int] = 0

        salary: Optional[float] = None

        joining_date: Optional[date] = None

        status: Optional[str] = "Active"

        aadhaar_number: Optional[str] = None
        pan_number: Optional[str] = None

        profile_photo: Optional[str] = None