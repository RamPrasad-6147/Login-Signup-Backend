from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas import RegisterUser


router = APIRouter()


# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# REGISTER USER
# =========================================================

@router.post("/register")
def register_user(
    user: RegisterUser,
    db: Session = Depends(get_db)
):

    # =====================================================
    # CHECK DUPLICATE EMAIL
    # =====================================================

    existing_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_email:

        return {
            "success": False,
            "message": "Email already registered."
        }


    # =====================================================
    # CHECK DUPLICATE PHONE
    # =====================================================

    existing_phone = (
        db.query(User)
        .filter(User.phone == user.phone)
        .first()
    )

    if existing_phone:

        return {
            "success": False,
            "message": "Phone number already exists."
        }


    # =====================================================
    # HASH PASSWORD
    # =====================================================

    hashed_password = pwd_context.hash(
        user.password
    )


    # =====================================================
    # CREATE NEW USER
    # =====================================================

    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        city=user.city,
        state=user.state,
        country=user.country,
        password=hashed_password
    )


    # =====================================================
    # SAVE USER TO DATABASE
    # =====================================================

    try:

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

    except IntegrityError:

        # Roll back failed database transaction
        db.rollback()

        # Check email again
        existing_email = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_email:

            return {
                "success": False,
                "message": "Email already registered."
            }


        # Check phone again
        existing_phone = (
            db.query(User)
            .filter(User.phone == user.phone)
            .first()
        )

        if existing_phone:

            return {
                "success": False,
                "message": "Phone number already exists."
            }


        return {
            "success": False,
            "message": "Unable to register user."
        }


    # =====================================================
    # SUCCESS RESPONSE
    # =====================================================

    return {
        "success": True,
        "message": "Registration successful!",

        "user": {
            "user_id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "phone": new_user.phone,
            "city": new_user.city,
            "state": new_user.state,
            "country": new_user.country
        }
    }