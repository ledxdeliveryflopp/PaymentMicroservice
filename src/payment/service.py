import uuid
from dataclasses import dataclass
import requests
from yookassa import Payment
from yookassa import Configuration
from src.payment.models import PaymentModel
from src.payment.repository import PaymentRepository
from src.payment.schemas import PaymentBaseSchemas, PaymentCheckSchemas
from src.settings.exceptions import UserDontExist, PaymentObjectDontExist, PaymentDontVerify, \
    BadPaymentId, UsersDontExist, PaymentDontExist
from src.settings.service import SessionService
from src.settings.settings import settings

Configuration.account_id = settings.yookassa_settings.account_id
Configuration.secret_key = settings.yookassa_settings.secret_key


@dataclass
class PaymentService:
    """Сервис заказов"""
    session_service: SessionService
    payment_repository: PaymentRepository

    async def create_payment_and_url(self, payment_schemas: PaymentBaseSchemas):
        """Создания ссылки для оплаты и данных для заказа"""
        token_data = await self.payment_repository.get_token_payload()
        user_email = token_data.get("email")
        user = await self.payment_repository.get_user_by_email(email=user_email)
        if not user:
            raise UserDontExist
        payment_object = await self.payment_repository.find_payment_object_by_id(
            id=payment_schemas.payment_object_id)
        if not payment_object:
            raise PaymentObjectDontExist
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": f"{payment_object.price}",
                "currency": "RUB"
            },
            "description": f"Заказ на сумму {payment_object.price} на аккаунт {user.email}",
            "metadata": {
                "payment_object_title": f"{payment_object.title}",
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url"
            },
        }, idempotence_key)
        yookassa_confirmation_url = payment.confirmation.confirmation_url
        yookassa_payment_id = payment.id
        db_payment = PaymentModel(code=yookassa_payment_id, user_id=user.id,
                                  price=payment_object.price, payment_object_id=payment_object.id)
        await self.session_service.save_update_object(save_object=db_payment)
        return {"confirmation_url": yookassa_confirmation_url, "payment_id": yookassa_payment_id}

    async def __check_yookassa_payment(self, code: str):
        """Проверка платежа на стороне Yookassa"""
        payment_in_db = await self.payment_repository.find_payment_by_code(code=code)
        idempotence_key = str(uuid.uuid4())
        try:
            response = Payment.capture(
                code,
                {
                    "amount": {
                        "value": f"{payment_in_db.price}",
                        "currency": "RUB"
                    }
                }, idempotence_key)
            return response["status"]
        except requests.exceptions.HTTPError:
            raise PaymentDontVerify

    async def verify_payment(self, check_schemas: PaymentCheckSchemas):
        """Проверка платежа не стороне сервиса"""
        payment_yookassa = await self.__check_yookassa_payment(code=check_schemas.payment_code)
        if not payment_yookassa or payment_yookassa is False:
            raise BadPaymentId
        if payment_yookassa != "succeeded":
            raise PaymentDontVerify
        token_data = await self.payment_repository.get_token_payload()
        user_email = token_data.get("email")
        user = await self.payment_repository.get_user_by_email(email=user_email)
        if not user:
            raise UsersDontExist
        payment_db = await self.payment_repository.find_payment_by_code(code=check_schemas.payment_code)
        if not payment_db:
            raise PaymentDontExist
        setattr(payment_db, "status", "success")
        await self.session_service.save_update_object(save_object=payment_db)
        return {"detail": "success"}

    async def get_current_user_payments(self):
        """Все платежи текущего пользователя"""
        token_data = await self.payment_repository.get_token_payload()
        user_email = token_data.get("email")
        user = await self.payment_repository.get_user_by_email(email=user_email)
        if not user:
            raise UserDontExist
        return user
