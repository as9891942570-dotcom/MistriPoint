from pydantic import BaseModel
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
    profile_image: str
    aadhaar_front: str
    aadhaar_back: str