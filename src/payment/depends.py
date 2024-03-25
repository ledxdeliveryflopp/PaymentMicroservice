from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.payment.repository import PaymentRepository
from src.payment.service import PaymentService
from src.settings.depends import get_session, get_session_service
from src.settings.service import SessionService


async def get_payment_service(request: Request, session: AsyncSession = Depends(get_session),
                              session_service: SessionService = Depends(get_session_service)):
    payment_repository = PaymentRepository(session=session, request=request)
    payment_service = PaymentService(payment_repository=payment_repository,
                                     session_service=session_service)
    return payment_service
