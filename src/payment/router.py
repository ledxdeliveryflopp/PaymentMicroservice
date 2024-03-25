from fastapi import APIRouter, Depends
from src.payment.depends import get_payment_service
from src.payment.schemas import PaymentBaseSchemas, PaymentCheckSchemas, AllUserPayments
from src.payment.service import PaymentService

payment_router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)


@payment_router.post('/create-payment-url/')
async def create_payment_url_router(payment_schemas: PaymentBaseSchemas,
                                    payment: PaymentService = Depends(get_payment_service)):
    """Роутер создания ссылки для оплаты"""
    return await payment.create_payment_and_url(payment_schemas=payment_schemas)


@payment_router.post('/verify-payment/')
async def verify_payment_router(check_schemas: PaymentCheckSchemas,
                                payment: PaymentService = Depends(get_payment_service)):
    """Роутер подтверждения оплаты"""
    return await payment.verify_payment(check_schemas=check_schemas)


@payment_router.get('/get-user-payments/', response_model=AllUserPayments)
async def get_current_user_payments_router(payment: PaymentService = Depends(get_payment_service)):
    """Роутер всех заказов пользователя"""
    return await payment.get_current_user_payments()
