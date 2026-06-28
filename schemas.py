from pydantic import BaseModel
from datetime import date
from typing import List


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