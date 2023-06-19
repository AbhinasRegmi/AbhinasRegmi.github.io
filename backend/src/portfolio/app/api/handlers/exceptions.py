from fastapi import HTTPException, status


class UploadSecretInvalidError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your secret is not valid. Try again with correct secret."
        )

class InvalidEmailError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email provided. Try again with correct email."
        )