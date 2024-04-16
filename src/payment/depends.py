from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.payment.service import PaymentService
from src.settings.depends import get_session


async def get_payment_service(request: Request, session: AsyncSession = Depends(get_session)) -> object:
    """Инициализация сервиса оплаты"""
    payment_service = PaymentService(session=session, request=request)
    return payment_service
