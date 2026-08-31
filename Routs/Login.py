from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas import LoginUser


router = APIRouter()


# =========================
# PASSWORD HASHING
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================
# LOGIN API
# =========================

@router.post("/login")
def login_user(
    user: LoginUser,
    db: Session = Depends(get_db)
):

    # =========================
    # FIND USER BY EMAIL
    # =========================

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )


    # =========================
    # EMAIL NOT FOUND
    # =========================

    if not existing_user:

        return {
            "success": False,
            "message": "Invalid email or password."
        }


    # =========================
    # VERIFY PASSWORD
    # =========================

    password_correct = pwd_context.verify(
        user.password,
        existing_user.password
    )


    # =========================
    # PASSWORD INCORRECT
    # =========================

    if not password_correct:

        return {
            "success": False,
            "message": "Invalid email or password."
        }


    # =========================
    # LOGIN SUCCESSFUL
    # =========================

    return {
        "success": True,
        "message": "Login successful!",

        "user_id": existing_user.id,

        "name": existing_user.name,

        "email": existing_user.email,

        "phone": existing_user.phone,

        "city": existing_user.city,

        "state": existing_user.state,

        "country": existing_user.country
    }