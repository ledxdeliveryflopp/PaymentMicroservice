from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.settings.db import Base


class PaymentModel(Base):
    """Модель оплаты"""
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    number = Column(String, index=True)
    user_id = Column(Integer,  ForeignKey("user.id"))

    user = relationship("UserModel", lazy="selectin", back_populates="payments")


class UserModel(Base):
    """Модель пользователей"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    payments = relationship(PaymentModel, lazy="selectin", back_populates="user")
