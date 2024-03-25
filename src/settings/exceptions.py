from typing import Any
from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class UserDontExist(DetailedHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User don't exist."


class UsersDontExist(DetailedHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "No users in system."


class BadRole(DetailedHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Current user don't have permission."


class PaymentObjectDontExist(DetailedHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Object don't exist."


class PaymentDontExist(DetailedHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment don't exist."


class BadPaymentId(DetailedHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment don't find."


class PaymentDontVerify(DetailedHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Not paid."
