from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.payment.router import payment_router

payment = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:7000",
    "http://localhost:6000",
    "http://localhost:5000",
]

payment.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

payment.include_router(payment_router)
