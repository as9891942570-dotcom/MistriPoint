from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, get_db
from schemas import *
from security import hash_password, verify_password
from models import User, Worker
from models import Skill, WorkerSkill, Worker
from schemas import SkillCreate, WorkerSkillCreate, WorkerSkillUpdate, WorkerStatusUpdate, AdminWorkerUpdate
from models import Job
from schemas import JobResponse



app = FastAPI( redoc_url=None)


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


@app.put("/worker-location/{worker_id}")
def update_worker_location(
    worker_id: int,
    data: WorkerLocation,
    db: Session = Depends(get_db)
):

    worker = db.query(Worker).filter(
        Worker.id == worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    worker.latitude = data.latitude
    worker.longitude = data.longitude

    db.commit()
    db.refresh(worker)

    return {
        "message": "Location updated successfully",
        "worker": worker
    }
@app.put("/worker-availability/{worker_id}")
def update_worker_availability(
    worker_id: int,
    data: WorkerAvailability,
    db: Session = Depends(get_db)
):

    worker = db.query(Worker).filter(
        Worker.id == worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    worker.is_available = data.is_available

    db.commit()
    db.refresh(worker)

    return {
        "message": "Availability updated successfully",
        "worker": worker
    }
@app.put("/worker-radius/{worker_id}")
def update_worker_radius(
    worker_id: int,
    data: WorkerRadius,
    db: Session = Depends(get_db)
):

    worker = db.query(Worker).filter(
        Worker.id == worker_id
    ).first()

    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker.working_radius = data.working_radius

    db.commit()
    db.refresh(worker)

    return {
        "message": "Working radius updated successfully",
        "worker": worker
    }
@app.put("/worker-preferred-area/{worker_id}")
def update_preferred_area(
    worker_id: int,
    data: WorkerPreferredArea,
    db: Session = Depends(get_db)
):

    worker = db.query(Worker).filter(
        Worker.id == worker_id
    ).first()

    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker.preferred_area = data.preferred_area

    db.commit()
    db.refresh(worker)

    return {
        "message": "Preferred area updated successfully",
        "worker": worker
    }
@app.post("/skills")
def create_skill(
    data: SkillCreate,
    db: Session = Depends(get_db)
):

    skill = Skill(
        skill_name=data.skill_name
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return {
        "message": "Skill Added Successfully",
        "skill_id": skill.id
    }
@app.get("/skills")
def get_skills(
    db: Session = Depends(get_db)
):

    skills = db.query(Skill).all()

    return skills
@app.post("/worker-skills")
def assign_skills(
    data: WorkerSkillCreate,
    db: Session = Depends(get_db)
):

    for skill_id in data.skill_ids:

        worker_skill = WorkerSkill(
            worker_id=data.worker_id,
            skill_id=skill_id
        )

        db.add(worker_skill)

    db.commit()

    return {
        "message": "Skills Assigned Successfully"
    }
@app.get("/worker-skills/{worker_id}")
def get_worker_skills(
    worker_id: int,
    db: Session = Depends(get_db)
):

    skills = (
        db.query(Skill.skill_name)
        .join(
            WorkerSkill,
            Skill.id == WorkerSkill.skill_id
        )
        .filter(
            WorkerSkill.worker_id == worker_id
        )
        .all()
    )

    return {
        "worker_id": worker_id,
        "skills": [s.skill_name for s in skills]
    }
@app.put("/worker-skills/{worker_id}")
def update_worker_skills(
    worker_id: int,
    data: WorkerSkillUpdate,
    db: Session = Depends(get_db)
):

    db.query(WorkerSkill).filter(
        WorkerSkill.worker_id == worker_id
    ).delete()

    for skill_id in data.skill_ids:

        db.add(
            WorkerSkill(
                worker_id=worker_id,
                skill_id=skill_id
            )
        )

    db.commit()

    return {
        "message": "Worker Skills Updated Successfully"
    }
@app.delete("/worker-skills/{worker_id}/{skill_id}")
def delete_worker_skill(
    worker_id: int,
    skill_id: int,
    db: Session = Depends(get_db)
):

    skill = db.query(WorkerSkill).filter(
        WorkerSkill.worker_id == worker_id,
        WorkerSkill.skill_id == skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill Not Found"
        )

    db.delete(skill)
    db.commit()

    return {
        "message": "Skill Deleted Successfully"
    }
@app.get("/jobs")
def get_all_jobs(
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).all()

    return jobs
@app.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job
@app.get("/jobs/category/{category_id}")
def get_jobs_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).filter(
        Job.category_id == category_id,
        Job.status == "Open"
    ).all()

    return jobs
@app.get("/jobs/city/{city}")
def get_jobs_by_city(
    city: str,
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).filter(
        Job.city == city,
        Job.status == "Open"
    ).all()

    return jobs
@app.get("/jobs/budget/{budget}")
def get_jobs_by_budget(
    budget: float,
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).filter(
        Job.budget >= budget,
        Job.status == "Open"
    ).all()

    return jobs
@app.get("/jobs/nearby/{worker_id}")
def nearby_jobs(
    worker_id: int,
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).filter(
        Job.status == "Open"
    ).all()

    return jobs
@app.get("/admin/workers")
def get_all_workers(db: Session = Depends(get_db)):

    workers = db.query(Worker).all()

    return {
        "message": "All Workers",
        "total_workers": len(workers),
        "data": workers
    }
@app.get("/admin/workers/{worker_id}")
def get_worker(worker_id: int, db: Session = Depends(get_db)):

    worker = db.query(Worker).filter(
        Worker.id == worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    return {
        "message": "Worker Details",
        "data": worker
    }
@app.put("/admin/workers/{worker_id}")
def update_worker(
    worker_id: int,
    data: AdminWorkerUpdate,
    db: Session = Depends(get_db)
):

    worker = db.query(Worker).filter(
        Worker.id == worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    worker.name = data.name
    worker.email = data.email
    worker.mobile = data.mobile
    worker.gender = data.gender
    worker.date_of_birth = data.date_of_birth
    worker.address = data.address
    worker.city = data.city
    worker.state = data.state
    worker.pincode = data.pincode
    worker.category_id = data.category_id
    worker.experience_years = data.experience_years
    worker.skills = data.skills
    worker.about = data.about
    worker.aadhaar_number = data.aadhaar_number
    worker.profile_image = data.profile_image
    worker.aadhaar_front = data.aadhaar_front
    worker.aadhaar_back = data.aadhaar_back

    db.commit()
    db.refresh(worker)

    return {
        "message": "Worker updated successfully",
        "data": worker
    }
@app.put("/admin/workers/{worker_id}/status")
def update_worker_status(
    worker_id: int,
    data: WorkerStatusUpdate,
    db: Session = Depends(get_db)
):

    worker = db.query(Worker).filter(
        Worker.id == worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    if data.status not in ["Pending", "Approved", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Pending, Approved or Rejected"
        )

    worker.status = data.status

    db.commit()
    db.refresh(worker)

    return {
        "message": "Worker status updated successfully",
        "status": worker.status
    }
@app.delete("/admin/workers/{worker_id}")
def delete_worker(
    worker_id: int,
    db: Session = Depends(get_db)
):

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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mistri:app", host="127.0.0.1", port=8000, reload=True)