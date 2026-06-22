from fastapi import FastAPI, HTTPException
from database import SessionLocal
from schemas import *
from models import User
from security import hash_password, verify_password

app = FastAPI()


@app.post("/register")
def register(data: RegisterRequest):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.mobile == data.mobile
        ).first()

        if user:
            raise HTTPException(
                status_code=400,
                detail="Mobile already exists"
            )

        new_user = User(
            mobile=data.mobile,
            password_hash=hash_password(
                data.password
            )
        )

        db.add(new_user)
        db.commit()

        return {
            "message":
            "User Registered Successfully"
        }

    finally:
        db.close()


@app.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.mobile == data.mobile
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid Credentials"
            )

        if not verify_password(
            data.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid Credentials"
            )

        return {
            "message":
            "Login Successful",
            "user_id": user.id
        }

    finally:
        db.close()


@app.put("/change-password")
def change_password(
    data: ChangePasswordRequest
):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.mobile == data.mobile
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User Not Found"
            )

        if not verify_password(
            data.old_password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=400,
                detail="Old Password Incorrect"
            )

        user.password_hash = hash_password(
            data.new_password
        )

        db.commit()

        return {
            "message":
            "Password Changed Successfully"
        }

    finally:
        db.close()


@app.get("/profile/{mobile}")
def get_profile(mobile: str):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.mobile == mobile
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User Not Found"
            )

        return {
            "id": user.id,
            "mobile": user.mobile,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at
        }

    finally:
        db.close()


@app.post("/logout")
def logout():

    return {
        "message":
        "Logout Successful"
    }