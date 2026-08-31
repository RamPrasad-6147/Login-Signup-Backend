from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

from Routs.Registration import router as registration_router
from Routs.Login import router as login_router


app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register API
app.include_router(registration_router)

# Login API
app.include_router(login_router)


@app.get("/")
def home():
    return {
        "message": "FastAPI Backend is Running"
    }