from decimal import Decimal
from pydantic import BaseModel


class PaymentBaseSchemas(BaseModel):
    """Схема для создания заказа и ссылки"""
    payment_object_id: int


class PaymentCheckSchemas(BaseModel):
    """Схема для проверки статуса платежа"""
    payment_code: str


class PaymentObjectsSchemas(BaseModel):
    """Схема объекта оплаты"""
    title: str
    description: str
    price: Decimal


class UserPaymentSchemas(BaseModel):
    """Схема заказа"""
    code: str
    price: Decimal
    status: str
    payments_object: PaymentObjectsSchemas


class AllUserPayments(BaseModel):
    """Схема всех заказов пользователя"""
    email: str
    payments: list[UserPaymentSchemas]
