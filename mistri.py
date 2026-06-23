from fastapi import FastAPI, HTTPException
from database import SessionLocal
from schemas import *
from security import hash_password, verify_password
from models import User, WorkerProfile
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


@app.post("/logout/{user_id}")
def logout(user_id: int):
    return {
        "message": "Logout Successful",
        "user_id": user_id
    }



@app.post("/worker-profile")
def create_worker_profile(
    data: WorkerProfileSchema
):

    db = SessionLocal()

    try:

        profile = WorkerProfile(
            **data.dict()
        )

        db.add(profile)
        db.commit()

        return {
            "message":
            "Worker Profile Created Successfully"
        }

    finally:
        db.close()


@app.get("/worker-profile/{user_id}")
def get_worker_profile(user_id: int):

    db = SessionLocal()

    try:

        profile = db.query(
            WorkerProfile
        ).filter(
            WorkerProfile.user_id == user_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        return profile

    finally:
        db.close()

@app.put("/worker-profile/{user_id}")
def update_worker_profile(
    user_id: int,
    data: WorkerProfileSchema
):

    db = SessionLocal()

    try:

        profile = db.query(
            WorkerProfile
        ).filter(
            WorkerProfile.user_id == user_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        for key, value in data.dict().items():
            setattr(profile, key, value)

        db.commit()

        return {
            "message":
            "Profile Updated Successfully"
        }

    finally:
        db.close()

@app.delete("/worker-profile/{user_id}")
def delete_worker_profile(user_id: int):

    db = SessionLocal()

    try:

        profile = db.query(
            WorkerProfile
        ).filter(
            WorkerProfile.user_id == user_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        db.delete(profile)
        db.commit()

        return {
            "message":
            "Profile Deleted Successfully"
        }

    finally:
        db.close()