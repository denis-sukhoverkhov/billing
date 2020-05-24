from app.config import settings
from app.service_layer import crud
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status
from tests.helpers import random_email


def test_api_create_user(
    client: TestClient, db: Session
) -> None:
    email = random_email()
    data = {"email": email, }
    r = client.post(
        f"{settings.API_V1_STR}/users/", json=data,
    )
    assert r.status_code == status.HTTP_201_CREATED
    created_user = r.json()

    user = crud.user.get_by_email(db, email=email)
    assert user.email == created_user["email"]

    wallet_list = crud.wallet.get_by_user_id(db, user_id=user.id)
    assert len(wallet_list) == 1
    assert wallet_list[0].balance == 0
