from fastapi import HTTPException, status

class InvalidEmailError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email supplied."
        )

class EmailServiceBusyError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Email server busy try again later."
        )

class TryAnotherEmailError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to find this email. Try with another email."
        )