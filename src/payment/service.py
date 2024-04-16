import uuid
from dataclasses import dataclass
import requests
from yookassa import Payment
from yookassa import Configuration
from src.payment.models import PaymentModel
from src.payment.repository import PaymentRepository
from src.payment.schemas import PaymentBaseSchemas, PaymentCheckSchemas
from src.settings.exceptions import UserDontExist, PaymentObjectDontExist, BadPaymentId, \
    UsersDontExist, PaymentDontExist
from src.settings.settings import settings

Configuration.account_id = settings.yookassa_settings.account_id
Configuration.secret_key = settings.yookassa_settings.secret_key


@dataclass
class PaymentService(PaymentRepository):
    """Сервис заказов"""

    async def create_payment_and_url(self, payment_schemas: PaymentBaseSchemas) -> dict:
        """Создания ссылки для оплаты и данных для заказа"""
        token_data = await self.get_token_payload()
        user_email = token_data.get("email")
        user = await self.get_user_by_email(email=user_email)
        if not user:
            raise UserDontExist
        payment_object = await self.find_payment_object_by_id(
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
        await self.create_object(save_object=db_payment)
        return {"confirmation_url": yookassa_confirmation_url, "payment_id": yookassa_payment_id}

    async def __check_yookassa_payment(self, code: str) -> str:
        """Проверка платежа на стороне Yookassa"""
        payment_in_db = await self.find_payment_by_code(code=code)
        if not payment_in_db:
            raise BadPaymentId
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
            return "canceled"

    async def verify_payment(self, check_schemas: PaymentCheckSchemas) -> dict:
        """Проверка платежа не стороне сервиса"""
        payment_yookassa = await self.__check_yookassa_payment(code=check_schemas.payment_code)
        print(payment_yookassa)
        if not payment_yookassa or payment_yookassa is False:
            raise BadPaymentId
        token_data = await self.get_token_payload()
        user_email = token_data.get("email")
        user = await self.get_user_by_email(email=user_email)
        if not user:
            raise UsersDontExist
        payment_db = await self.find_payment_by_code(code=check_schemas.payment_code)
        if not payment_db:
            raise PaymentDontExist
        if payment_yookassa != "succeeded":
            setattr(payment_db, "status", "canceled")
            await self.create_object(save_object=payment_db)
            return {"detail": "payment canceled"}
        setattr(payment_db, "status", "success")
        await self.create_object(save_object=payment_db)
        return {"detail": "success"}

    async def get_current_user_payments(self) -> object:
        """Все платежи текущего пользователя"""
        token_data = await self.get_token_payload()
        user_email = token_data.get("email")
        user = await self.get_user_by_email(email=user_email)
        if not user:
            raise UserDontExist
        return user
