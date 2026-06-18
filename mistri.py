from fastapi import FastAPI, HTTPException
from database import get_db_connection
from schemas import *

app = FastAPI()

@app.post("/register")
def register(data: RegisterRequest):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE mobile=%s",
        (data.mobile,)
    )

    if cursor.fetchone():
        raise HTTPException(
            status_code=400,
            detail="Mobile already exists"
        )

    cursor.execute(
        """
        INSERT INTO users
        (mobile,password_hash)
        VALUES(%s,%s)
        """,
        (data.mobile, data.password)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "User Registered Successfully"}
@app.post("/login")
def login(data: LoginRequest):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE mobile=%s
        AND password_hash=%s
        """,
        (data.mobile, data.password)
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    cursor.execute(
        """
        INSERT INTO login_history(user_id)
        VALUES(%s)
        """,
        (user["id"],)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Login Successful",
        "user_id": user["id"]
    }
@app.put("/change-password")
def change_password(data: ChangePasswordRequest):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE mobile=%s
        AND password_hash=%s
        """,
        (
            data.mobile,
            data.old_password
        )
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Old Password Incorrect"
        )

    cursor.execute(
        """
        UPDATE users
        SET password_hash=%s
        WHERE mobile=%s
        """,
        (
            data.new_password,
            data.mobile
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Password Changed Successfully"
    }
@app.get("/profile/{mobile}")
def get_profile(mobile: str):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        id,
        mobile,
        is_active,
        is_verified,
        created_at
        FROM users
        WHERE mobile=%s
        """,
        (mobile,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    return user
@app.post("/logout")
def logout(user_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE login_history
        SET logout_time=NOW()
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Logout Successful"
    }