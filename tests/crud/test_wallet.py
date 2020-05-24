from app.domain.entities.wallet import WalletCreate
from app.service_layer import crud
from sqlalchemy.orm import Session

# from app import crud
from tests.helpers import create_random_user, create_random_user_with_wallet


def test_create_wallet(db: Session) -> None:

    random_user = create_random_user(db)
    wallet_in = WalletCreate(user_id=random_user.id, balance=777)
    wallet = crud.wallet.create(db, obj_in=wallet_in)

    assert wallet.balance == wallet_in.balance
    assert wallet.user_id == random_user.id
    assert wallet.is_active is True
    assert wallet.created_at is not None

    # check wallet history
    wallet_history_list = crud.wallet_history.get_by(db, wallet_id=wallet.id)
    assert len(wallet_history_list) == 1
    wallet_history = wallet_history_list[0]
    assert wallet_history.balance == wallet_in.balance


def test_atomic_enroll_balance(db: Session) -> None:

    start_balance = 0
    user, old_wallet = create_random_user_with_wallet(db, balance=start_balance)

    enroll_delta = 159
    enrolled_wallet = crud.wallet.atomic_enroll_balance(db, obj_id=old_wallet.id, amount=enroll_delta)

    wallet = crud.wallet.get_by_pk(db, pk=old_wallet.id)
    assert wallet.balance == start_balance + enroll_delta
    assert wallet.updated_at is not None

    # check wallet history
    wallet_history_list = crud.wallet_history.get_by(db, wallet_id=enrolled_wallet.id)
    assert len(wallet_history_list) == 2
    assert wallet_history_list[0].balance == start_balance
    assert wallet_history_list[1].balance == start_balance + enroll_delta
