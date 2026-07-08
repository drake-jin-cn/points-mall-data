import time

import jwt as pyjwt
import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

TEST_SECRET = "test-jwt-secret-change-me-please"


def make_token(payload: dict = None, secret: str = TEST_SECRET, exp_offset: int = 900) -> str:
    base = {
        "sub": 1,
        "email": "admin@pointsmall.com",
        "roles": ["admin"],
        "iat": int(time.time()),
        "exp": int(time.time()) + exp_offset,
    }
    if payload:
        base.update(payload)
    return pyjwt.encode(base, secret, algorithm="HS256")


@pytest.fixture
def test_app(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", TEST_SECRET)

    from app.dependencies.auth import verify_token

    app = FastAPI()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/protected", dependencies=[Depends(verify_token)])
    def protected():
        return {"message": "authorized"}

    return TestClient(app)


# AC-01: valid token passes through
def test_valid_bearer_token_passes(test_app):
    token = make_token()
    response = test_app.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "authorized"}


# AC-02: missing Authorization header → 401 data-6001
def test_missing_authorization_header_returns_401(test_app):
    response = test_app.get("/protected")
    assert response.status_code == 401
    body = response.json()
    assert body["detail"]["code"] == "data-6001"
    assert body["detail"]["message"] == "Unauthorized"
    assert body["detail"]["data"] is None


# AC-02: non-Bearer format → 401
def test_non_bearer_format_returns_401(test_app):
    response = test_app.get("/protected", headers={"Authorization": "Token something"})
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "data-6001"


# AC-03: malformed token → 401
def test_invalid_token_returns_401(test_app):
    response = test_app.get("/protected", headers={"Authorization": "Bearer not.a.valid.jwt"})
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "data-6001"


# AC-03: expired token → 401
def test_expired_token_returns_401(test_app):
    expired_token = make_token(exp_offset=-100)
    response = test_app.get("/protected", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "data-6001"


# AC-03: wrong secret → 401
def test_wrong_secret_token_returns_401(test_app):
    token = make_token(secret="wrong-secret-that-is-long-enough-here")
    response = test_app.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "data-6001"


# AC-04: /health has no auth requirement
def test_health_route_accessible_without_token(test_app):
    response = test_app.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
