import os

import jwt as pyjwt
from fastapi import Header, HTTPException


def verify_token(authorization: str = Header(default=None)) -> dict:
    """
    FastAPI dependency that validates a Bearer JWT in the Authorization header.
    Returns the decoded payload dict on success.
    Raises HTTP 401 with code 'data-6001' on any validation failure.
    """
    _unauthorized = HTTPException(
        status_code=401,
        detail={"code": "data-6001", "message": "Unauthorized", "data": None},
    )

    if not authorization or not authorization.startswith("Bearer "):
        raise _unauthorized

    token = authorization[7:]
    secret = os.environ.get("JWT_SECRET", "")
    if not secret:
        raise _unauthorized

    try:
        payload = pyjwt.decode(token, secret, algorithms=["HS256"], options={"verify_sub": False})
        return payload
    except pyjwt.PyJWTError:
        raise _unauthorized
