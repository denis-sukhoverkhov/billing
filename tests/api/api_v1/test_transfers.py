from app.config import settings
from app.service_layer import crud
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.helpers import create_random_user_with_wallet


def test_api_payment_transfer_from_source_wallet_to_receiver_wallet(
    client: TestClient, db: Session
) -> None:

    start_balance1 = 23
    _, wallet_source = create_random_user_with_wallet(db, balance=start_balance1)

    start_balance2 = 7
    _, wallet_receiver = create_random_user_with_wallet(db, balance=start_balance2)

    amount = 3
    data = {"amount": amount, }
    r = client.post(
        f"{settings.API_V1_STR}/transfers/from/{wallet_source.id}/to/{wallet_receiver.id}", json=data,
    )
    assert r.status_code == status.HTTP_200_OK
    enrolled_wallet_json = r.json()
    assert start_balance1 - amount == enrolled_wallet_json['balance']

    db.expire_all()

    wallet_receiver = crud.wallet.get_by_pk(db, pk=wallet_receiver.id)
    assert wallet_receiver.balance == start_balance2 + amount

    wallet_source = crud.wallet.get_by_pk(db, pk=wallet_source.id)
    assert wallet_source.balance == start_balance1 - amount


