from fastapi import FastAPI
from src.payment.router import payment_router

payment = FastAPI()

payment.include_router(payment_router)
