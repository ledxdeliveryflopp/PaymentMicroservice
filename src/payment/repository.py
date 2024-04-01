from dataclasses import dataclass
from jose import jwt
from sqlalchemy import Select
from starlette.requests import Request
from src.payment.models import PaymentObjectModel, PaymentModel, UserModel
from src.settings.exceptions import UserDontExist
from src.settings.service import SessionService
from src.settings.settings import settings


@dataclass
class PaymentRepository(SessionService):
    """Репазиторий для взаимодествия заказов с бд"""
    request: Request

    async def get_token_payload(self):
        """Email и роль пользователя из токена"""
        header_token = self.request.headers.get('Authorization')
        header_token = header_token.replace("Bearer ", "")
        token_payload = jwt.decode(token=header_token, key=settings.jwt_settings.jwt_secret,
                                   algorithms=settings.jwt_settings.jwt_algorithm)
        user_email = token_payload.get("user_email")
        return {'email': user_email}

    async def get_user_by_email(self, email: str):
        """Получить пользователя по Email"""
        user = await self.session.execute(Select(UserModel).filter(UserModel.email == email))
        if not user:
            raise UserDontExist
        return user.scalar()

    async def find_payment_object_by_id(self, id: int):
        """Получить заказ по ID"""
        payment_object = await self.session.execute(Select(PaymentObjectModel).filter(PaymentObjectModel.id == id))
        return payment_object.scalar()

    async def find_payment_by_code(self, code: str):
        """Найти заказ по коду"""
        payment = await self.session.execute(Select(PaymentModel).filter(PaymentModel.code == code))
        return payment.scalar()
