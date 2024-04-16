from sqlalchemy import Column, String, DECIMAL, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.settings.models import DefaultModel


class PaymentObjectModel(DefaultModel):
    """Абстрактная модель объекта для оплаты"""
    __tablename__ = "object"

    title = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, unique=False, nullable=False, index=True)
    price = Column(DECIMAL, nullable=False)


class PaymentModel(DefaultModel):
    """Модель данных о покупке"""
    __tablename__ = "payment"

    code = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    status = Column(String, default="pending", nullable=False)
    payment_object_id = Column(Integer, ForeignKey("object.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("UserModel", lazy="selectin", back_populates="payments", foreign_keys=[user_id])
    payments_object = relationship("PaymentObjectModel", lazy="selectin", foreign_keys=[payment_object_id])


class Role:
    admin: str = "admin"
    manager: str = "manager"
    user: str = "user"


class UserModel(DefaultModel):
    """Модель пользователей"""
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default=Role.user)

    payments = relationship("PaymentModel", lazy="selectin", back_populates="user")


