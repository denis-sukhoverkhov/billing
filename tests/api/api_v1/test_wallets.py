from app.config import settings
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.helpers import create_random_user_with_wallet


def test_api_enroll_cash_to_wallet(
    client: TestClient, db: Session
) -> None:

    start_balance = 20
    user, wallet = create_random_user_with_wallet(db, balance=start_balance)

    enrolled_amount = 45
    data = {"amount": enrolled_amount, }
    r = client.post(
        f"{settings.API_V1_STR}/wallets/{wallet.id}/enroll", json=data,
    )
    assert r.status_code == status.HTTP_200_OK
    enrolled_wallet_json = r.json()
    assert start_balance + enrolled_amount == enrolled_wallet_json['balance']
