from pydantic import BaseModel

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