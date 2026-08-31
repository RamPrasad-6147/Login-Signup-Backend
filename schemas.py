from pydantic import BaseModel, EmailStr, Field, field_validator
import re


# =========================================================
# REGISTER USER
# =========================================================

class RegisterUser(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str

    city: str = Field(
        min_length=2,
        max_length=100
    )

    state: str = Field(
        min_length=2,
        max_length=100
    )

    country: str = Field(
        min_length=2,
        max_length=100
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )


    # =====================================================
    # PHONE VALIDATION
    # =====================================================

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        value = value.strip()

        # Indian 10-digit mobile number
        if not re.fullmatch(r"[6-9]\d{9}", value):

            raise ValueError(
                "Phone number must be a valid 10-digit number."
            )

        return value


    # =====================================================
    # PASSWORD VALIDATION
    # =====================================================

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        # Uppercase
        if not re.search(r"[A-Z]", value):

            raise ValueError(
                "Password must contain at least one uppercase letter."
            )


        # Lowercase
        if not re.search(r"[a-z]", value):

            raise ValueError(
                "Password must contain at least one lowercase letter."
            )


        # Number
        if not re.search(r"\d", value):

            raise ValueError(
                "Password must contain at least one number."
            )


        # Special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):

            raise ValueError(
                "Password must contain at least one special character."
            )

        return value


# =========================================================
# LOGIN USER
# =========================================================

class LoginUser(BaseModel):

    email: EmailStr

    password: str