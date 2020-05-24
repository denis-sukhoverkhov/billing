from app.domain.entities import UserCreate
from app.service_layer import use_cases, crud
from sqlalchemy.orm import Session

# from app import crud
from tests.helpers import random_email, create_random_user_with_wallet


def test_create_user_with_wallet(db: Session) -> None:
    email = random_email()
    user_in = UserCreate(email=email, )

    user = use_cases.create_user_with_wallet(db, user_in=user_in)

    assert user.email == email
    assert user.is_active is True
    assert user.created_at is not None

    user_wallet = user.wallet[0]
    assert user_wallet.balance == 0


def test_transfer_payment_from_source_to_receiver(db: Session) -> None:

    start_balance1 = 500
    user1, wallet_source = create_random_user_with_wallet(db, balance=start_balance1)

    start_balance2 = 10
    user2, wallet_receiver = create_random_user_with_wallet(db, balance=start_balance2)

    transfer_amount = 37
    use_cases.transfer_payment_from_source_to_receiver(
        db, wallet_id_source=wallet_source.id, wallet_id_receiver=wallet_receiver.id, amount=transfer_amount)

    wallet_source = crud.wallet.get_by_pk(db, pk=wallet_source.id)
    assert wallet_source.balance == start_balance1 - transfer_amount

    wallet_receiver = crud.wallet.get_by_pk(db, pk=wallet_receiver.id)
    assert wallet_receiver.balance == start_balance2 + transfer_amount

    # check history for wallet_source
    wallet_source_history_list = crud.wallet_history.get_by(db, wallet_id=wallet_source.id)
    assert len(wallet_source_history_list) == 2
    assert wallet_source_history_list[0].balance == start_balance1
    assert wallet_source_history_list[1].balance == start_balance1 - transfer_amount

    # check history for wallet_receiver
    wallet_receiver_history_list = crud.wallet_history.get_by(db, wallet_id=wallet_receiver.id)
    assert len(wallet_receiver_history_list) == 2
    assert wallet_receiver_history_list[0].balance == start_balance2
    assert wallet_receiver_history_list[1].balance == start_balance2 + transfer_amount
