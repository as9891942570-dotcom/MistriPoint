from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, get_db
from schemas import *
from security import hash_password, verify_password
from models import User, Worker
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
    data: WorkerCreate,
    db: Session = Depends(get_db)
):

    worker = Worker(
        name=data.name,
        email=data.email,
        mobile=data.mobile,
        gender=data.gender,
        date_of_birth=data.date_of_birth,
        address=data.address,
        city=data.city,
        state=data.state,
        pincode=data.pincode,
        category_id=data.category_id,
        experience_years=data.experience_years,
        skills=data.skills,
        about=data.about,
        aadhaar_number=data.aadhaar_number,
        status="Pending",
        profile_image=data.profile_image,
        aadhaar_front=data.aadhaar_front,
        aadhaar_back=data.aadhaar_back
    )

    db.add(worker)
    db.commit()
    db.refresh(worker)

    return {
        "message": "Worker Profile Created Successfully",
        "worker_id": worker.id
    }
@app.get("/worker-profile/{worker_id}")
def get_worker_profile(worker_id: int):

    db = SessionLocal()

    try:
        profile = db.query(Worker).filter(
            Worker.id == worker_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Worker not found"
            )

        return profile

    finally:
        db.close()

@app.get("/worker-profiles")
def get_all_worker_profiles():

    db = SessionLocal()

    try:
        workers = db.query(Worker).all()

        if not workers:
            raise HTTPException(
                status_code=404,
                detail="No workers found"
            )

        return workers

    finally:
        db.close()

@app.put("/worker-profile/{worker_id}")
def update_worker_profile(worker_id: int, worker_data: WorkerCreate):

    db = SessionLocal()

    try:
        worker = db.query(Worker).filter(
            Worker.id == worker_id
        ).first()

        if not worker:
            raise HTTPException(
                status_code=404,
                detail="Worker not found"
            )

        worker.name = worker_data.name
        worker.email = worker_data.email
        worker.mobile = worker_data.mobile
        worker.gender = worker_data.gender
        worker.date_of_birth = worker_data.date_of_birth
        worker.address = worker_data.address
        worker.city = worker_data.city
        worker.state = worker_data.state
        worker.pincode = worker_data.pincode
        worker.category_id = worker_data.category_id
        worker.experience_years = worker_data.experience_years
        worker.skills = worker_data.skills
        worker.about = worker_data.about
        worker.aadhaar_number = worker_data.aadhaar_number
        worker.profile_image = worker_data.profile_image
        worker.aadhaar_front = worker_data.aadhaar_front
        worker.aadhaar_back = worker_data.aadhaar_back

        db.commit()
        db.refresh(worker)

        return {
            "message": "Worker updated successfully",
            "data": worker
        }

    finally:
        db.close()
@app.delete("/worker-profile/{worker_id}")
def delete_worker_profile(worker_id: int):

    db = SessionLocal()

    try:
        worker = db.query(Worker).filter(
            Worker.id == worker_id
        ).first()

        if not worker:
            raise HTTPException(
                status_code=404,
                detail="Worker not found"
            )

        db.delete(worker)
        db.commit()

        return {
            "message": "Worker deleted successfully"
        }

    finally:
        db.close()